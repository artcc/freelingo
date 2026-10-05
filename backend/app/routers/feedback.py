"""Feedback router — feature requests and bug reports with voting and comments."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.core.limiter import limiter
from app.models.feedback import FeedbackComment, FeedbackEntry, FeedbackReadState, FeedbackVote
from app.models.user import User
from app.schemas.feedback import (
    FeedbackAuthor,
    FeedbackCommentCreate,
    FeedbackCommentOut,
    FeedbackCommentsResponse,
    FeedbackEntryCreate,
    FeedbackEntryDetail,
    FeedbackEntryOut,
    FeedbackReadResponse,
    FeedbackStatusUpdate,
    FeedbackUnreadSummary,
    FeedbackVoteResponse,
    PaginatedFeedbackResponse,
)
from app.services import email_service
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


async def _get_entry_or_404(entry_id: int, db: AsyncSession) -> FeedbackEntry:
    entry = await db.get(FeedbackEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="feedback_entry_not_found")
    return entry


async def _mark_entry_read(
    entry_id: int,
    user_id: int,
    db: AsyncSession,
    read_at: datetime | None = None,
) -> FeedbackReadState:
    now = read_at or _utcnow()
    read_state = await db.scalar(
        select(FeedbackReadState).where(
            FeedbackReadState.entry_id == entry_id,
            FeedbackReadState.user_id == user_id,
        )
    )
    if read_state:
        read_state.last_read_at = now
    else:
        read_state = FeedbackReadState(entry_id=entry_id, user_id=user_id, last_read_at=now)
        db.add(read_state)
    return read_state


async def _get_unread_count(user_id: int, db: AsyncSession) -> int:
    read_state = FeedbackReadState
    comment_activity = exists().where(
        FeedbackComment.entry_id == FeedbackEntry.id,
        FeedbackComment.author_id != user_id,
        or_(
            read_state.last_read_at.is_(None),
            FeedbackComment.created_at > read_state.last_read_at,
        ),
    )
    entry_activity = or_(
        read_state.last_read_at.is_(None),
        FeedbackEntry.created_at > read_state.last_read_at,
    )
    stmt = (
        select(func.count(FeedbackEntry.id))
        .outerjoin(
            read_state,
            (read_state.entry_id == FeedbackEntry.id) & (read_state.user_id == user_id),
        )
        .where(
            or_(
                and_(FeedbackEntry.author_id != user_id, entry_activity),
                comment_activity,
            )
        )
    )
    return await db.scalar(stmt) or 0


async def _get_unread_entry_ids(
    user_id: int,
    entry_ids: list[int],
    db: AsyncSession,
) -> set[int]:
    if not entry_ids:
        return set()

    read_state = FeedbackReadState
    comment_activity = exists().where(
        FeedbackComment.entry_id == FeedbackEntry.id,
        FeedbackComment.author_id != user_id,
        or_(
            read_state.last_read_at.is_(None),
            FeedbackComment.created_at > read_state.last_read_at,
        ),
    )
    entry_activity = or_(
        read_state.last_read_at.is_(None),
        FeedbackEntry.created_at > read_state.last_read_at,
    )
    stmt = (
        select(FeedbackEntry.id)
        .outerjoin(
            read_state,
            (read_state.entry_id == FeedbackEntry.id) & (read_state.user_id == user_id),
        )
        .where(
            FeedbackEntry.id.in_(entry_ids),
            or_(
                and_(FeedbackEntry.author_id != user_id, entry_activity),
                comment_activity,
            ),
        )
    )
    return set((await db.execute(stmt)).scalars().all())


async def _build_entry_out(
    entry: FeedbackEntry,
    current_user: User,
    db: AsyncSession,
) -> FeedbackEntryOut:
    """Enrich a single FeedbackEntry with author info, vote status, and comment count.

    Used for single-entry responses (create, vote, status update).
    For lists use _build_entries_out which batches all DB round-trips.
    """
    author = await db.get(User, entry.author_id)
    voted = await db.scalar(
        select(FeedbackVote).where(
            FeedbackVote.entry_id == entry.id,
            FeedbackVote.user_id == current_user.id,
        )
    )
    comment_count = await db.scalar(
        select(func.count())
        .select_from(FeedbackComment)
        .where(FeedbackComment.entry_id == entry.id)
    )
    unread_ids = await _get_unread_entry_ids(current_user.id, [entry.id], db)
    return FeedbackEntryOut(
        id=entry.id,
        type=entry.type,
        title=entry.title,
        description=entry.description,
        status=entry.status,
        author=FeedbackAuthor(
            id=author.id,
            username=author.username,
            display_name=author.display_name,
            role=author.role,
        ),
        vote_count=entry.vote_count,
        voted_by_me=voted is not None,
        unread_by_me=entry.id in unread_ids,
        comment_count=comment_count or 0,
        created_at=entry.created_at,
    )


async def _build_entries_out(
    entries: list[FeedbackEntry],
    current_user: User,
    db: AsyncSession,
) -> list[FeedbackEntryOut]:
    """Build FeedbackEntryOut objects for a list of entries using batch queries.

    Replaces N×3 individual queries with 4 queries total regardless of list size:
      1. (already done by caller) paginate()
      2. SELECT users WHERE id IN (author_ids)
      3. SELECT entry_id FROM feedback_votes WHERE entry_id IN (...) AND user_id = me
      4. SELECT entry_id, count(*) FROM feedback_comments WHERE entry_id IN (...) GROUP BY entry_id
    """
    if not entries:
        return []

    entry_ids = [e.id for e in entries]
    author_ids = list({e.author_id for e in entries})

    # Batch fetch all unique authors
    author_rows = (await db.execute(select(User).where(User.id.in_(author_ids)))).scalars().all()
    authors: dict[int, User] = {u.id: u for u in author_rows}

    # Batch fetch which entries the current user has voted for
    voted_ids: set[int] = set(
        (
            await db.execute(
                select(FeedbackVote.entry_id).where(
                    FeedbackVote.entry_id.in_(entry_ids),
                    FeedbackVote.user_id == current_user.id,
                )
            )
        )
        .scalars()
        .all()
    )

    # Batch fetch comment counts grouped by entry
    count_rows = (
        await db.execute(
            select(FeedbackComment.entry_id, func.count().label("cnt"))
            .where(FeedbackComment.entry_id.in_(entry_ids))
            .group_by(FeedbackComment.entry_id)
        )
    ).all()
    comment_counts: dict[int, int] = {row.entry_id: row.cnt for row in count_rows}
    unread_ids = await _get_unread_entry_ids(current_user.id, entry_ids, db)

    result: list[FeedbackEntryOut] = []
    for entry in entries:
        author = authors.get(entry.author_id)
        if author is None:
            # Author was deleted; skip to avoid AttributeError on orphaned entries
            continue
        result.append(
            FeedbackEntryOut(
                id=entry.id,
                type=entry.type,
                title=entry.title,
                description=entry.description,
                status=entry.status,
                author=FeedbackAuthor(
                    id=author.id,
                    username=author.username,
                    display_name=author.display_name,
                    role=author.role,
                ),
                vote_count=entry.vote_count,
                voted_by_me=entry.id in voted_ids,
                unread_by_me=entry.id in unread_ids,
                comment_count=comment_counts.get(entry.id, 0),
                created_at=entry.created_at,
            )
        )
    return result


async def _build_comments_out(
    comments: list[FeedbackComment],
    db: AsyncSession,
) -> list[FeedbackCommentOut]:
    """Build FeedbackCommentOut objects for a list of comments using a single batch query.

    Replaces one db.get(User) per comment with a single IN query for all unique authors.
    """
    if not comments:
        return []

    author_ids = list({c.author_id for c in comments})
    author_rows = (await db.execute(select(User).where(User.id.in_(author_ids)))).scalars().all()
    authors: dict[int, User] = {u.id: u for u in author_rows}

    result: list[FeedbackCommentOut] = []
    for c in comments:
        author = authors.get(c.author_id)
        if author is None:
            continue
        result.append(
            FeedbackCommentOut(
                id=c.id,
                entry_id=c.entry_id,
                author=FeedbackAuthor(
                    id=author.id,
                    username=author.username,
                    display_name=author.display_name,
                    role=author.role,
                ),
                body=c.body,
                created_at=c.created_at,
            )
        )
    return result


# ---------------------------------------------------------------------------
# GET /api/feedback/unread-summary — unread activity count
# ---------------------------------------------------------------------------


@router.get("/unread-summary", response_model=FeedbackUnreadSummary)
@limiter.limit("60/minute")
async def get_unread_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackUnreadSummary:
    """Return the number of feedback threads with unread activity for the current user."""
    return FeedbackUnreadSummary(unread_count=await _get_unread_count(current_user.id, db))


# ---------------------------------------------------------------------------
# GET /api/feedback — list entries (paginated, filtered, sorted)
# ---------------------------------------------------------------------------


@router.get("", response_model=PaginatedFeedbackResponse)
@limiter.limit("60/minute")
async def list_feedback(
    request: Request,
    type: str | None = Query(default=None, pattern="^(feature|bug)$"),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        pattern="^(pending|planned|in_progress|done|declined)$",
    ),
    q: str | None = Query(default=None, max_length=100),
    sort: str = Query(default="votes", pattern="^(votes|date)$"),
    order: str = Query(default="desc", pattern="^(asc|desc)$"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedFeedbackResponse:
    """Return a paginated list of feedback entries."""
    stmt = select(FeedbackEntry)
    if type:
        stmt = stmt.where(FeedbackEntry.type == type)
    if status_filter:
        stmt = stmt.where(FeedbackEntry.status == status_filter)
    else:
        stmt = stmt.where(FeedbackEntry.status.notin_(["done", "declined"]))
    if q and q.strip():
        term = f"%{q.strip()}%"
        stmt = stmt.join(User, FeedbackEntry.author_id == User.id).where(
            or_(
                FeedbackEntry.title.ilike(term),
                FeedbackEntry.description.ilike(term),
                User.username.ilike(term),
                User.display_name.ilike(term),
            )
        )

    # Sorting
    if sort == "votes":
        sort_col = FeedbackEntry.vote_count
    else:
        sort_col = FeedbackEntry.created_at

    if order == "desc":
        stmt = stmt.order_by(sort_col.desc(), FeedbackEntry.id.desc())
    else:
        stmt = stmt.order_by(sort_col.asc(), FeedbackEntry.id.asc())

    entries, total = await paginate(db, stmt, skip, limit)

    items = await _build_entries_out(entries, current_user, db)

    return PaginatedFeedbackResponse(items=items, total=total, skip=skip, limit=limit)


# ---------------------------------------------------------------------------
# POST /api/feedback — create entry
# ---------------------------------------------------------------------------


@router.post("", response_model=FeedbackEntryOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
async def create_feedback(
    request: Request,
    body: FeedbackEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackEntryOut:
    """Create a new feature request or bug report."""
    entry = FeedbackEntry(
        type=body.type,
        title=body.title.strip(),
        description=body.description.strip(),
        status="pending",
        author_id=current_user.id,
        vote_count=0,
        created_at=_utcnow(),
    )
    db.add(entry)
    await db.flush()
    await _mark_entry_read(entry.id, current_user.id, db, entry.created_at)
    await db.commit()
    await db.refresh(entry)
    admin_locale = await db.scalar(
        select(User.native_language).where(User.role == "admin").order_by(User.id.asc()).limit(1)
    )
    asyncio.create_task(
        email_service.send_feedback_notification(
            entry_type=entry.type,
            title=entry.title,
            description=entry.description,
            author_username=current_user.username,
            entry_id=entry.id,
            locale=admin_locale or "en",
        )
    )
    return await _build_entry_out(entry, current_user, db)


# ---------------------------------------------------------------------------
# POST /api/feedback/{entry_id}/read — mark entry read
# ---------------------------------------------------------------------------


@router.post("/{entry_id}/read", response_model=FeedbackReadResponse)
@limiter.limit("60/minute")
async def mark_feedback_read(
    request: Request,
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackReadResponse:
    """Mark a single feedback thread as read for the current user."""
    await _get_entry_or_404(entry_id, db)
    read_state = await _mark_entry_read(entry_id, current_user.id, db)
    await db.commit()
    await db.refresh(read_state)
    return FeedbackReadResponse(entry_id=entry_id, last_read_at=read_state.last_read_at)


# ---------------------------------------------------------------------------
# GET /api/feedback/{entry_id} — entry detail with comments
# ---------------------------------------------------------------------------


@router.get("/{entry_id}", response_model=FeedbackEntryDetail)
@limiter.limit("60/minute")
async def get_feedback(
    request: Request,
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackEntryDetail:
    """Return a single feedback entry with its full comment thread."""
    entry = await _get_entry_or_404(entry_id, db)
    base = await _build_entry_out(entry, current_user, db)

    # Fetch comments ordered by created_at ASC
    result = await db.execute(
        select(FeedbackComment)
        .where(FeedbackComment.entry_id == entry_id)
        .order_by(FeedbackComment.created_at.asc())
    )
    comments_raw = result.scalars().all()
    comments = await _build_comments_out(list(comments_raw), db)

    return FeedbackEntryDetail(**base.model_dump(), comments=comments)


# ---------------------------------------------------------------------------
# DELETE /api/feedback/{entry_id} — delete entry (author or admin)
# ---------------------------------------------------------------------------


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def delete_feedback(
    request: Request,
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a feedback entry. Author can delete their own; admin can delete any."""
    entry = await _get_entry_or_404(entry_id, db)
    if entry.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    await db.delete(entry)
    await db.commit()


# ---------------------------------------------------------------------------
# POST /api/feedback/{entry_id}/vote — toggle vote (features only)
# ---------------------------------------------------------------------------


@router.post("/{entry_id}/vote", response_model=FeedbackVoteResponse)
@limiter.limit("60/minute")
async def toggle_vote(
    request: Request,
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackVoteResponse:
    """Toggle the current user's vote on a feature request. Bugs cannot be voted."""
    entry = await _get_entry_or_404(entry_id, db)
    if entry.type != "feature":
        raise HTTPException(status_code=400, detail="only_features_are_voteable")

    existing = await db.scalar(
        select(FeedbackVote).where(
            FeedbackVote.entry_id == entry_id,
            FeedbackVote.user_id == current_user.id,
        )
    )

    if existing:
        # Remove vote
        await db.delete(existing)
        entry.vote_count = max(0, entry.vote_count - 1)
        voted = False
    else:
        # Add vote
        db.add(FeedbackVote(entry_id=entry_id, user_id=current_user.id, created_at=_utcnow()))
        entry.vote_count += 1
        voted = True

    await db.commit()
    await db.refresh(entry)
    return FeedbackVoteResponse(voted=voted, vote_count=entry.vote_count)


# ---------------------------------------------------------------------------
# PATCH /api/feedback/{entry_id}/status — update status (admin only)
# ---------------------------------------------------------------------------


@router.patch("/{entry_id}/status", response_model=FeedbackEntryOut)
@limiter.limit("60/minute")
async def update_status(
    request: Request,
    entry_id: int,
    body: FeedbackStatusUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> FeedbackEntryOut:
    """Update the status of a feedback entry. Admin only."""
    entry = await _get_entry_or_404(entry_id, db)
    entry.status = body.status
    await db.commit()
    await db.refresh(entry)
    return await _build_entry_out(entry, current_user, db)


# ---------------------------------------------------------------------------
# GET /api/feedback/{entry_id}/comments — list comments
# ---------------------------------------------------------------------------


@router.get("/{entry_id}/comments", response_model=FeedbackCommentsResponse)
@limiter.limit("60/minute")
async def list_comments(
    request: Request,
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackCommentsResponse:
    """Return all comments for a feedback entry ordered by date ascending."""
    await _get_entry_or_404(entry_id, db)

    result = await db.execute(
        select(FeedbackComment)
        .where(FeedbackComment.entry_id == entry_id)
        .order_by(FeedbackComment.created_at.asc())
    )
    comments_raw = result.scalars().all()
    items = await _build_comments_out(list(comments_raw), db)

    return FeedbackCommentsResponse(items=items, total=len(items))


# ---------------------------------------------------------------------------
# POST /api/feedback/{entry_id}/comments — add comment
# ---------------------------------------------------------------------------


@router.post(
    "/{entry_id}/comments",
    response_model=FeedbackCommentOut,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/hour")
async def add_comment(
    request: Request,
    entry_id: int,
    body: FeedbackCommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackCommentOut:
    """Add a comment to a feedback entry."""
    await _get_entry_or_404(entry_id, db)

    comment = FeedbackComment(
        entry_id=entry_id,
        author_id=current_user.id,
        body=body.body.strip(),
        created_at=_utcnow(),
    )
    db.add(comment)
    await db.flush()
    await _mark_entry_read(entry_id, current_user.id, db, comment.created_at)
    await db.commit()
    await db.refresh(comment)

    return FeedbackCommentOut(
        id=comment.id,
        entry_id=comment.entry_id,
        author=FeedbackAuthor(
            id=current_user.id,
            username=current_user.username,
            display_name=current_user.display_name,
            role=current_user.role,
        ),
        body=comment.body,
        created_at=comment.created_at,
    )


# ---------------------------------------------------------------------------
# DELETE /api/feedback/{entry_id}/comments/{comment_id} — delete comment
# ---------------------------------------------------------------------------


@router.delete(
    "/{entry_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("60/minute")
async def delete_comment(
    request: Request,
    entry_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a comment. Author can delete their own; admin can delete any."""
    await _get_entry_or_404(entry_id, db)

    comment = await db.get(FeedbackComment, comment_id)
    if not comment or comment.entry_id != entry_id:
        raise HTTPException(status_code=404, detail="comment_not_found")
    if comment.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="forbidden")

    await db.delete(comment)
    await db.commit()
