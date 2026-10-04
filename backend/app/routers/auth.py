import base64
import hashlib
import json
import os
import uuid
from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse
from redis.asyncio import Redis
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, get_redis
from app.core.limiter import limiter
from app.core.security import create_access_token, create_refresh_token, dummy_verify, hash_password, verify_password
from app.models.refresh_token import RefreshToken
from app.models.user import AdminBootstrapClaim, User
from app.models.user_language import UserLanguage
from app.schemas.auth import ForgotPasswordRequest, LoginRequest, RegisterRequest, RegisterResponse, ResetPasswordRequest, TokenResponse, UserResponse, UserUpdateRequest
from app.services import email_service
from app.services.subscription_trial_service import issue_go_trial

logger = get_logger(__name__)
_AVATARS_DIR: str | None = None
router = APIRouter(prefix="/api/auth", tags=["auth"])
# Lua works on Redis versions older than GETDEL and consumes exactly once.
_CONSUME_REFRESH_LUA = "local v=redis.call('GET',KEYS[1]); if v then redis.call('DEL',KEYS[1]) end; return v"


async def _claim_registration_role(db: AsyncSession) -> str:
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        insert = pg_insert
    elif dialect == "sqlite":
        insert = sqlite_insert
    else:
        raise RuntimeError("Atomic admin bootstrap requires PostgreSQL or SQLite")
    result = await db.execute(insert(AdminBootstrapClaim).values(id=1)
        .on_conflict_do_nothing(index_elements=[AdminBootstrapClaim.id]).returning(AdminBootstrapClaim.id))
    if result.scalar_one_or_none() is None:
        return "user"
    existing_user = await db.scalar(select(User.id).limit(1))
    return "admin" if settings.FIRST_USER_IS_ADMIN and existing_user is None else "user"


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def _store_refresh_token(redis: Redis | None, token: str, user_id: int, ttl: int,
                               db: AsyncSession | None = None, session_version: int | None = None) -> None:
    if session_version is None:
        user = await db.get(User, user_id) if db is not None else None
        session_version = user.session_version if user is not None else 0
    if redis is not None:
        await redis.setex(f"refresh:{token}", ttl, json.dumps({"uid": user_id, "sv": session_version}))
        return
    if db is None:
        raise RuntimeError("Desktop refresh token storage requires a database session")
    now = datetime.now(UTC).replace(tzinfo=None)
    await db.execute(delete(RefreshToken).where(RefreshToken.expires_at <= now))
    db.add(RefreshToken(token_hash=_hash_refresh_token(token), user_id=user_id,
                        session_version=session_version, expires_at=now + timedelta(seconds=ttl)))
    await db.commit()


async def _consume_refresh_token(redis: Redis | None, token: str, db: AsyncSession | None = None) -> int | None:
    if redis is not None:
        raw = await redis.eval(_CONSUME_REFRESH_LUA, 1, f"refresh:{token}")
        if not raw:
            return None
        try:
            value = json.loads(raw)
            # Upgrade compatibility: old Redis values contained just user_id.
            if isinstance(value, dict):
                user_id, version = int(value["uid"]), int(value["sv"])
            else:
                user_id, version = int(value), 0
        except (ValueError, TypeError, KeyError):
            return None
    else:
        if db is None:
            raise RuntimeError("Desktop refresh token storage requires a database session")
        now = datetime.now(UTC).replace(tzinfo=None)
        result = await db.execute(delete(RefreshToken).where(
            RefreshToken.token_hash == _hash_refresh_token(token), RefreshToken.expires_at > now,
        ).returning(RefreshToken.user_id, RefreshToken.session_version))
        row = result.one_or_none()
        if row is None:
            await db.commit()
            return None
        user_id, version = int(row.user_id), int(row.session_version)
    if db is not None:
        # Serialize rotation against password revision changes on both dialects.
        await db.execute(update(User).where(User.id == user_id).values(session_version=User.session_version))
        user = await db.scalar(select(User).where(User.id == user_id).execution_options(populate_existing=True))
        if user is None or not user.is_active or user.session_version != version:
            await db.commit()  # Persist consumption of invalid/revoked credentials.
            return None
    return user_id


async def _delete_refresh_token(redis: Redis | None, token: str, db: AsyncSession | None = None) -> None:
    if redis is not None:
        await redis.delete(f"refresh:{token}")
        return
    if db is None:
        raise RuntimeError("Desktop refresh token storage requires a database session")
    await db.execute(delete(RefreshToken).where(RefreshToken.token_hash == _hash_refresh_token(token)))
    await db.commit()


async def _change_password(db: AsyncSession, user: User, password: str) -> None:
    # Same transaction: update the password, increment the revision, remove SQL
    # refresh tokens. Redis tokens become unusable via revision checks as well.
    hashed = hash_password(password)
    await db.execute(update(User).where(User.id == user.id).values(
        hashed_password=hashed, session_version=User.session_version + 1,
    ).execution_options(synchronize_session=False))
    await db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))


def _require_redis(redis: Redis | None, feature: str) -> Redis:
    if redis is None:
        raise HTTPException(status_code=503, detail=f"{feature} requires Redis in the current configuration")
    return redis


@router.post("/register", response_model=RegisterResponse)
@limiter.limit("5/minute")
async def register(request: Request, data: RegisterRequest, response: Response,
                   db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    if not settings.ALLOW_REGISTRATION:
        if not data.invite_token:
            raise HTTPException(status_code=403, detail="Registration is closed")
        redis_client = _require_redis(redis, "Invite registration")
        valid = await redis_client.get(f"invite:{data.invite_token}")
        if not valid:
            raise HTTPException(status_code=403, detail="Invalid or expired invite")
        await redis_client.delete(f"invite:{data.invite_token}")
    if settings.BLOCKED_EMAIL_DOMAINS:
        email_domain = data.email.split("@")[-1].lower()
        if email_domain in [d.lower() for d in settings.BLOCKED_EMAIL_DOMAINS]:
            raise HTTPException(status_code=422, detail="Email domain not allowed")
    hashed_password = hash_password(data.password)
    role = await _claim_registration_role(db)
    existing = await db.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Username already taken")
    email_check = await db.execute(select(User).where(User.email == data.email))
    if email_check.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already taken")
    user = User(username=data.username, email=data.email, display_name=data.display_name or data.username,
                hashed_password=hashed_password, native_language=data.native_language,
                target_language=data.target_language, role=role, is_active=True, is_verified=not settings.EMAIL_ENABLED)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await issue_go_trial(db, user)
    access_token = create_access_token(user.id, user.role, user.session_version)
    refresh_token = create_refresh_token()
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    await _store_refresh_token(redis, refresh_token, user.id, ttl, db, user.session_version)
    response.set_cookie("refresh_token", refresh_token, httponly=True,
                        secure=settings.COOKIE_SECURE and not settings.DESKTOP_MODE, samesite="lax", max_age=ttl)
    if user.email and settings.EMAIL_ENABLED:
        verify_token = str(uuid.uuid4())
        redis_client = _require_redis(redis, "Email verification")
        await redis_client.setex(f"verify_email:{verify_token}", 86400, str(user.id))
        await email_service.send_verification_email(user.email, user.display_name, verify_token, locale=user.native_language)
        await email_service.send_welcome_email(user.email, user.display_name, locale=user.native_language)
    return RegisterResponse(id=user.id, username=user.username, role=user.role, access_token=access_token)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, data: LoginRequest, response: Response,
                db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if user:
        password_ok = verify_password(data.password, user.hashed_password)
    else:
        dummy_verify()
        password_ok = False
    if not password_ok or not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user.last_login = datetime.now(UTC).replace(tzinfo=None)
    await db.commit()
    access_token = create_access_token(user.id, user.role, user.session_version)
    refresh_token = create_refresh_token()
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    await _store_refresh_token(redis, refresh_token, user.id, ttl, db, user.session_version)
    response.set_cookie("refresh_token", refresh_token, httponly=True,
                        secure=settings.COOKIE_SECURE and not settings.DESKTOP_MODE, samesite="lax", max_age=ttl)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("60/minute")
async def refresh(request: Request, response: Response, redis: Redis | None = Depends(get_redis),
                  db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    user_id = await _consume_refresh_token(redis, token, db)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid, revoked or expired refresh token")
    user = await db.get(User, user_id)
    # Defend here as well; _consume already checks under the account lock.
    if user is None or not user.is_active:
        await db.commit()
        raise HTTPException(status_code=401, detail="User not found or inactive")
    new_refresh = create_refresh_token()
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    access = create_access_token(user.id, user.role, user.session_version)
    await _store_refresh_token(redis, new_refresh, user.id, ttl, db, user.session_version)
    await db.commit()
    response.set_cookie("refresh_token", new_refresh, httponly=True,
                        secure=settings.COOKIE_SECURE and not settings.DESKTOP_MODE, samesite="lax", max_age=ttl)
    return {"access_token": access, "token_type": "bearer"}


@router.post("/logout")
@limiter.limit("60/minute")
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db),
                 redis: Redis | None = Depends(get_redis)):
    token = request.cookies.get("refresh_token")
    if token:
        await _delete_refresh_token(redis, token, db)
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}


@router.get("/me", response_model=UserResponse)
@limiter.limit("60/minute")
async def get_me(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        await issue_go_trial(db, current_user)
    except Exception:
        await db.rollback()
        await db.refresh(current_user)
        logger.warning("Could not issue Go trial during account read", exc_info=True)
    return current_user


@router.patch("/me", response_model=UserResponse)
@limiter.limit("60/minute")
async def update_me(request: Request, data: UserUpdateRequest, response: Response,
                    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if data.display_name is not None:
        current_user.display_name = data.display_name
    if data.email is not None and data.email != current_user.email:
        dup = await db.execute(select(User).where(User.email == data.email))
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already taken")
        current_user.email = data.email
    if data.native_language is not None:
        current_user.native_language = data.native_language
    if data.target_language is not None:
        current_user.target_language = data.target_language
        from app.services.user_language_service import get_user_languages
        user_langs = await get_user_languages(db, current_user.id)
        existing = next((ul for ul in user_langs if ul.target_language == data.target_language), None)
        if existing:
            from app.services.user_language_service import switch_language
            await switch_language(db, current_user.id, data.target_language)
        else:
            new_prefix = data.target_language.split("-")[0]
            same_base = next((ul for ul in user_langs if ul.target_language.split("-")[0] == new_prefix), None)
            if same_base:
                await db.execute(update(UserLanguage).where(UserLanguage.user_id == current_user.id,
                    UserLanguage.is_active.is_(True)).values(is_active=False))
                same_base.target_language = data.target_language
                same_base.is_active = True
            else:
                from app.services.user_language_service import add_language
                await add_language(db, current_user.id, data.target_language)
    if data.ui_locale is not None:
        current_user.ui_locale = data.ui_locale if data.ui_locale.strip() else None
    if data.conversation_max_duration is not None:
        current_user.conversation_max_duration = data.conversation_max_duration
    if data.conversation_inactivity_timeout is not None:
        current_user.conversation_inactivity_timeout = data.conversation_inactivity_timeout
    if data.bio is not None:
        current_user.bio = data.bio if data.bio.strip() else None
    if data.learning_goals is not None:
        current_user.learning_goals = json.dumps(data.learning_goals)
    if data.password is not None:
        await db.flush()
        await _change_password(db, current_user, data.password)
    await db.commit()
    await db.refresh(current_user)
    if data.password is not None:
        # Explicit policy: revoke every old session, including this one.
        response.delete_cookie("refresh_token")
    return current_user


_MAX_AVATAR_BYTES = 2 * 1024 * 1024
_ALLOWED_AVATAR_TYPES = {"image/jpeg", "image/png"}


def _avatars_dir() -> str:
    data_dir = settings.DATA_DIR or os.path.join(os.path.expanduser("~"), "JUBA-LISAN")
    return _AVATARS_DIR or os.path.join(data_dir, "avatars")


def _avatar_path_from_reference(avatar: str | None) -> str | None:
    if not avatar or not avatar.startswith("/api/avatars/"):
        return None
    filename = avatar.split("?")[0].split("/")[-1]
    if filename != os.path.basename(filename):
        return None
    return os.path.join(_avatars_dir(), filename)


def _validate_avatar_bytes(content_type: str | None, data: bytes) -> str:
    if content_type not in _ALLOWED_AVATAR_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG images are allowed")
    if content_type == "image/jpeg" and data.startswith(b"\xff\xd8\xff"):
        if len(data) < 4 or not data.endswith(b"\xff\xd9"):
            raise HTTPException(status_code=400, detail="Invalid image file")
        return "jpg"
    if content_type == "image/png" and data.startswith(b"\x89PNG\r\n\x1a\n"):
        if len(data) < 24 or data[12:16] != b"IHDR":
            raise HTTPException(status_code=400, detail="Invalid image file")
        width, height = int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
        if width <= 0 or height <= 0:
            raise HTTPException(status_code=400, detail="Invalid image file")
        return "png"
    raise HTTPException(status_code=400, detail="Invalid image file")


@router.post("/me/avatar", response_model=UserResponse)
@limiter.limit("60/minute")
async def upload_avatar(request: Request, file: UploadFile = File(...), current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    data = await file.read(_MAX_AVATAR_BYTES + 1)
    if len(data) > _MAX_AVATAR_BYTES:
        raise HTTPException(status_code=400, detail="Image too large (max 2 MB)")
    ext = _validate_avatar_bytes(file.content_type, data)
    old_path = _avatar_path_from_reference(current_user.avatar)
    if old_path and os.path.exists(old_path):
        os.remove(old_path)
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(_avatars_dir(), filename)
    os.makedirs(_avatars_dir(), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(data)
    ts = int(datetime.now(UTC).timestamp() * 1000)
    current_user.avatar = f"/api/avatars/{filename}?v={ts}"
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/me/avatar-file", response_model=None)
@limiter.limit("60/minute")
async def get_avatar_file(request: Request, current_user: User = Depends(get_current_user)) -> Response:
    if not current_user.avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    if current_user.avatar.startswith("data:image/"):
        header, _, payload = current_user.avatar.partition(",")
        media_type = header.removeprefix("data:").split(";")[0]
        try:
            return Response(content=base64.b64decode(payload), media_type=media_type, headers={"Cache-Control": "private, no-store"})
        except Exception as exc:
            raise HTTPException(status_code=404, detail="Avatar not found") from exc
    if not current_user.avatar.startswith("/api/avatars/"):
        raise HTTPException(status_code=404, detail="Avatar not found")
    path = _avatar_path_from_reference(current_user.avatar)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Avatar not found")
    media_type = "image/jpeg" if os.path.basename(path).lower().endswith(".jpg") else "image/png"
    return FileResponse(path, media_type=media_type, headers={"Cache-Control": "private, no-store"})


@router.delete("/me/avatar", response_model=UserResponse)
@limiter.limit("60/minute")
async def delete_avatar(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    old_path = _avatar_path_from_reference(current_user.avatar)
    if old_path and os.path.exists(old_path):
        os.remove(old_path)
    current_user.avatar = None
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_me(request: Request, response: Response, current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Admin accounts cannot be self-deleted")
    token = request.cookies.get("refresh_token")
    if token:
        await _delete_refresh_token(redis, token, db)
    response.delete_cookie("refresh_token")
    old_path = _avatar_path_from_reference(current_user.avatar)
    if old_path and os.path.exists(old_path):
        os.remove(old_path)
    user_email, user_display_name, user_locale = current_user.email, current_user.display_name, current_user.native_language
    await db.delete(current_user)
    await db.commit()
    try:
        await email_service.send_account_deleted_email(user_email, user_display_name, user_locale)
    except Exception:
        logger.warning("Failed to send account-deleted email to %s", user_email)


@router.get("/quota")
@limiter.limit("60/minute")
async def get_my_quota(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                       redis: Redis | None = Depends(get_redis)):
    from app.services.quota_service import get_monthly_tokens_used, get_quota_status
    quota = await get_quota_status(redis, current_user.id, current_user.conversation_weekly_sessions,
                                   current_user.conversation_daily_minutes, current_user.conversation_weekly_minutes)
    tokens_used = await get_monthly_tokens_used(db, current_user.id)
    quota["tokens_this_month"] = tokens_used
    quota["tokens_monthly_limit"] = current_user.monthly_tokens_limit
    quota["tokens_unlimited"] = current_user.monthly_tokens_limit == 0
    return quota


@router.get("/verify-email")
@limiter.limit("60/minute")
async def verify_email(request: Request, token: str, db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    redis_client = _require_redis(redis, "Email verification")
    user_id_str = await redis_client.get(f"verify_email:{token}")
    if not user_id_str:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    user = await db.get(User, int(user_id_str))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    await db.commit()
    await redis_client.delete(f"verify_email:{token}")
    return {"detail": "Email verified successfully"}


@router.post("/resend-verification")
@limiter.limit("3/minute")
async def resend_verification(request: Request, current_user: User = Depends(get_current_user), redis: Redis | None = Depends(get_redis)):
    if current_user.is_verified:
        return {"detail": "Already verified"}
    if not current_user.email:
        raise HTTPException(status_code=400, detail="No email address on file")
    if not settings.EMAIL_ENABLED:
        raise HTTPException(status_code=503, detail="Email not configured")
    verify_token = str(uuid.uuid4())
    redis_client = _require_redis(redis, "Email verification")
    await redis_client.setex(f"verify_email:{verify_token}", 86400, str(current_user.id))
    await email_service.send_verification_email(current_user.email, current_user.display_name, verify_token, locale=current_user.native_language)
    return {"detail": "Verification email sent"}


@router.post("/forgot-password")
@limiter.limit("5/minute")
async def forgot_password(request: Request, data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if user and settings.EMAIL_ENABLED:
        reset_token = str(uuid.uuid4())
        redis_client = _require_redis(redis, "Password reset")
        await redis_client.setex(f"reset_password:{reset_token}", 3600, str(user.id))
        await email_service.send_reset_password_email(user.email, user.display_name, reset_token, locale=user.native_language)
    return {"detail": "If that email is registered you will receive a reset link shortly"}


@router.post("/reset-password")
@limiter.limit("5/minute")
async def reset_password(request: Request, data: ResetPasswordRequest, response: Response,
                         db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)):
    redis_client = _require_redis(redis, "Password reset")
    # Consume the token atomically (GET+DEL in one Redis call) before touching the
    # password, so two concurrent requests cannot both use it and a crash after the
    # commit cannot leave it valid until the TTL expires.
    user_id_str = await redis_client.eval(_CONSUME_REFRESH_LUA, 1, f"reset_password:{data.token}")
    if not user_id_str:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    try:
        user_id = int(user_id_str)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token") from None
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await _change_password(db, user, data.new_password)
    await db.commit()
    response.delete_cookie("refresh_token")
    return {"detail": "Password updated successfully"}
