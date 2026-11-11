from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource_native_help import ResourceNativeHelp


def calculate_source_hash(source: dict) -> str:
    payload = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


async def get_cached_native_help(
    db: AsyncSession,
    *,
    resource_type: str,
    resource_key: str,
    target_language: str,
    native_language: str,
    source_hash: str,
) -> ResourceNativeHelp | None:
    # Another request may have updated an entry already present in this session.
    result = await db.execute(
        select(ResourceNativeHelp)
        .where(
            ResourceNativeHelp.resource_type == resource_type,
            ResourceNativeHelp.resource_key == resource_key,
            ResourceNativeHelp.target_language == target_language,
            ResourceNativeHelp.native_language == native_language,
        )
        .execution_options(populate_existing=True)
    )
    cached = result.scalar_one_or_none()
    if cached and cached.source_hash == source_hash:
        return cached
    return None


async def upsert_native_help(
    db: AsyncSession,
    *,
    resource_type: str,
    resource_key: str,
    target_language: str,
    native_language: str,
    source_hash: str,
    content: dict,
) -> ResourceNativeHelp:
    result = await db.execute(
        select(ResourceNativeHelp).where(
            ResourceNativeHelp.resource_type == resource_type,
            ResourceNativeHelp.resource_key == resource_key,
            ResourceNativeHelp.target_language == target_language,
            ResourceNativeHelp.native_language == native_language,
        )
    )
    cached = result.scalar_one_or_none()
    now = datetime.now(UTC).replace(tzinfo=None)
    if cached:
        cached.source_hash = source_hash
        cached.content = content
        cached.updated_at = now
    else:
        cached = ResourceNativeHelp(
            resource_type=resource_type,
            resource_key=resource_key,
            target_language=target_language,
            native_language=native_language,
            source_hash=source_hash,
            content=content,
            created_at=now,
            updated_at=now,
        )
        db.add(cached)
    await db.commit()
    await db.refresh(cached)
    return cached


def native_help_lock_key(
    *,
    resource_type: str,
    resource_key: str,
    target_language: str,
    native_language: str,
) -> str:
    return f"native_help:{resource_type}:{target_language}:{native_language}:{resource_key}"
