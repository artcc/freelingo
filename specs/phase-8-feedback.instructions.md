---
description: "Phase 8 spec — Feedback board: feature requests, bug reports, voting, comments, and admin management."
applyTo: "backend/**, frontend/**"
---

# Phase 8 — Feedback Board

## Overview

A community feedback board where users can submit feature requests and bug reports, vote on suggestions, discuss entries via flat comment threads, and see a sidebar unread counter for new feedback activity. Admins manage entry status and can delete any entry or comment. Administrator-authored entries and replies carry an `ADMIN` badge beside the author's display name.

---

## Database models

### `feedback_entries`

- id — Type: integer; Constraints: PK, autoincrement; Notes: —
- type — Type: string(10); Constraints: NOT NULL, index; Notes: `"feature"` or `"bug"`
- title — Type: string(200); Constraints: NOT NULL; Notes: —
- description — Type: text; Constraints: NOT NULL; Notes: Max 5000 chars enforced by schema
- status — Type: string(20); Constraints: NOT NULL, default `"pending"`, index; Notes: `pending` \
- author_id — Type: integer; Constraints: NOT NULL, FK → users(CASCADE), index; Notes: —
- vote_count — Type: integer; Constraints: NOT NULL, default 0; Notes: Denormalised; updated atomically on vote toggle
- created_at — Type: datetime; Constraints: NOT NULL, index; Notes: UTC, tz-naive

### `feedback_votes`

- id — Type: integer; Constraints: PK, autoincrement; Notes: —
- entry_id — Type: integer; Constraints: NOT NULL, FK → feedback_entries(CASCADE), index; Notes: —
- user_id — Type: integer; Constraints: NOT NULL, FK → users(CASCADE), index; Notes: —
- created_at — Type: datetime; Constraints: NOT NULL; Notes: —

`UNIQUE(entry_id, user_id)` — `uq_feedback_vote`. Only feature entries can receive votes; the router rejects vote attempts on bugs with HTTP 400.

### `feedback_comments`

- id — Type: integer; Constraints: PK, autoincrement; Notes: —
- entry_id — Type: integer; Constraints: NOT NULL, FK → feedback_entries(CASCADE), index; Notes: —
- author_id — Type: integer; Constraints: NOT NULL, FK → users(CASCADE), index; Notes: —
- body — Type: text; Constraints: NOT NULL; Notes: Max 2000 chars enforced by schema
- created_at — Type: datetime; Constraints: NOT NULL; Notes: —

### `feedback_read_states`

- id — Type: integer; Constraints: PK, autoincrement; Notes: —
- entry_id — Type: integer; Constraints: NOT NULL, FK → feedback_entries(CASCADE), index; Notes: —
- user_id — Type: integer; Constraints: NOT NULL, FK → users(CASCADE), index; Notes: —
- last_read_at — Type: datetime; Constraints: NOT NULL; Notes: Per-user marker used by the unread counter

`UNIQUE(entry_id, user_id)` — `uq_feedback_read_state`. Read state is private to each authenticated user.

Cascade behaviour: deleting a `FeedbackEntry` cascades to all its `FeedbackVote`, `FeedbackComment`, and `FeedbackReadState` rows at the DB level (`ondelete="CASCADE"`).

---

## Alembic migration

`backend/alembic/versions/0020_feedback.py` — revision `0020_feedback`, down_revision `0019_reading`.

Creates `feedback_entries`, `feedback_votes`, `feedback_comments` with all indexes and the unique vote constraint. Fully reversible via `downgrade()`.

`backend/alembic/versions/0046_feedback_read_states.py` — revision `0046_feedback_read_states`, down_revision `0045_assessment_voice_trial`.

Creates `feedback_read_states` with `entry_id` and `user_id` indexes plus the unique per-user/per-thread read marker constraint. Fully reversible via `downgrade()`.

---

## Backend router

**File:** `backend/app/routers/feedback.py`  
**Prefix:** `/api/feedback`  
**Tag:** `feedback`

### Helpers

- `_utcnow()` — returns tz-naive UTC datetime (consistent with all other models).
- `_get_entry_or_404(entry_id, db)` — fetches `FeedbackEntry` by PK or raises HTTP 404.
- `_mark_entry_read(entry_id, user_id, db, read_at=None)` — creates or updates the current user's read marker for one feedback thread only.
- `_get_unread_count(user_id, db)` — counts feedback threads with unread activity from other users, including entries marked `done`. Counts threads, not individual comments.
- `_get_unread_entry_ids(user_id, entry_ids, db)` — batched helper used by list/detail mappers to expose `unread_by_me` on visible entries.
- `_build_entry_out(entry, current_user, db)` — enriches an ORM entry with `FeedbackAuthor` (fetched by PK), `voted_by_me` (scalar query), `unread_by_me` (read-state query), and `comment_count` (count query with `select_from`).

### Endpoints

- **GET `/`** — Rate limit: 60/min. Auth: get_current_user. Notes: Accepts `q` (title, description, username, or display name search; max 100 chars), `type`, `status` (alias for `status_filter`), `sort` (votes\|date), `order` (asc\|desc), `skip` (default 0), and `limit` (default 10, max 100). Entry ID is the deterministic secondary ordering criterion, in the same direction as the requested order, so ties cannot shuffle rows between offset pages. If `status` is omitted, `done` entries are excluded by default from both the public board and admin queue; they are returned only when `status=done` is explicitly requested. Count runs against `stmt.subquery()` for accurate filtered totals.
- **GET `/unread-summary`** — Rate limit: 60/min. Auth: get_current_user. Notes: Returns `{unread_count}` for the authenticated user's unread feedback threads. Activity by the same user does not count as unread for that user.
- **POST `/`** — Rate limit: 10/hour. Auth: get_current_user. Notes: Creates entry with status `pending`, marks it read for the author, returns HTTP 201, and fires an admin email notification (see below).
- **GET `/{id}`** — Rate limit: 60/min. Auth: get_current_user. Notes: Returns `FeedbackEntryDetail` with comments list (ordered by `created_at ASC`).
- **POST `/{id}/read`** — Rate limit: 60/min. Auth: get_current_user. Notes: Marks only that feedback thread as read for the current user. Returns `{entry_id, last_read_at}`.
- **DELETE `/{id}`** — Rate limit: 20/min. Auth: get_current_user. Notes: Allowed if `author_id == current_user.id` OR `current_user.role == "admin"`. Returns HTTP 204.
- **POST `/{id}/vote`** — Rate limit: 30/min. Auth: get_current_user. Notes: Toggle: if vote exists → delete + decrement `vote_count`; else → insert + increment. `max(0, ...)` guard prevents negative counts. Returns `{voted, vote_count}`.
- **PATCH `/{id}/status`** — Rate limit: 30/min. Auth: require_admin. Notes: Updates `status` field. Returns updated `FeedbackEntryOut`.
- **GET `/{id}/comments`** — Rate limit: 60/min. Auth: get_current_user. Notes: Returns `FeedbackCommentsResponse` with `total = len(items)`.
- **POST `/{id}/comments`** — Rate limit: 20/hour. Auth: get_current_user. Notes: Creates comment, marks the thread read for the author of the comment, returns HTTP 201 + `FeedbackCommentOut`.
- **DELETE `/{id}/comments/{cid}`** — Rate limit: 20/min. Auth: get_current_user. Notes: Validates `comment.entry_id == entry_id` to prevent cross-entry deletions. Allowed if author or admin. Returns HTTP 204.

---

## Schemas (`backend/app/schemas/feedback.py`)

- `FeedbackAuthor` — embedded author info: `id`, `username`, `display_name`, `role`. The live user role is resolved for entry and comment responses so clients can identify administrator-authored content. `from_attributes=True`.
- `FeedbackEntryCreate` — validates `type` pattern `^(feature|bug)$`, title 1–200, description 1–5000.
- `FeedbackCommentOut` — **defined before** `FeedbackEntryDetail` to avoid forward reference issues with Pydantic.
- `FeedbackUnreadSummary` — `{unread_count: int}`.
- `FeedbackReadResponse` — `{entry_id, last_read_at}`.
- `FeedbackEntryOut` — includes `voted_by_me: bool = False`, `unread_by_me: bool = False`, and `comment_count: int = 0` (injected server-side, not from ORM).
- `FeedbackEntryDetail(FeedbackEntryOut)` — adds `comments: list[FeedbackCommentOut] = []`. Built with `FeedbackEntryOut.model_dump()` + comment list.
- `PaginatedFeedbackResponse` — `{items, total, skip, limit}` — identical pattern to `PaginatedAdminUsersResponse`.
- `FeedbackVoteResponse` — `{voted: bool, vote_count: int}`.
- `FeedbackCommentCreate` — `body` 1–2000 chars.
- `FeedbackStatusUpdate` — validates `status` pattern `^(pending|planned|in_progress|done|declined)$`.

---

## Frontend

### `/feedback` (`frontend/src/app/(app)/feedback/page.tsx`)

**State:** `tab` (feature|bug), `sort` (votes|date), `statusFilter`, `entries[]`, `total`, `page`, `loading`, `error`, `showCreate`, `selectedEntry`, `deletePending`.

**Two views controlled by `selectedEntry`:**

1. **List view** — tabs, sort toggles, status dropdown filter, paginated card list, create modal trigger.
2. **Detail view** (`DetailView` component) — full description, vote button, delete button (author or admin), flat comment thread with add/delete, back button.

**Key design decisions:**

- Vote toggle is available both inline on list cards (without navigating to detail) and in the detail view.
- `getStatusLabel(status)` uses a lookup object (`{ pending: t('statusPending'), ... }`) — **not** string template manipulation — to avoid runtime errors with underscored keys like `in_progress`.
- `DetailView` receives `isAdmin` and `getStatusLabel` as props from the parent to avoid re-deriving them.
- `CreateModal` calls `onCreated()` with no arguments after a successful POST; the parent reloads with `loadEntries(0, tab, sort, statusFilter)`.
- Pagination: 10 entries per page with the identical two-effect pattern as `admin/users/page.tsx` — one effect on `page`, one effect on filters that resets to page 0 before loading.
- Default listing behavior: entries with `status=done` are hidden unless the status dropdown is set to Done.
- Admin users see delete button on all entries in both list and detail views; regular users only see it on their own entries.
- The shared `AdminAuthorBadge` renders a compact petroleum-blue `ADMIN` marker using `fl-accent` beside the author name in entry lists, entry detail metadata, and comment headers only when `author.role == "admin"`; normal users receive no role label.
- Feedback list items show a red unread label immediately to the right of the status badge when `unread_by_me` is true. This is independent from the feedback status and only reflects the current user's read state.
- Opening a detail view calls `POST /api/feedback/{entry_id}/read` and marks only that thread as read for the current user.

**Status badge colours (consistent with admin users page):**

- pending — Border: `border-fl-border`; Text: `text-fl-muted-2`
- planned — Border: `border-blue-500/40`; Text: `text-blue-400`
- in_progress — Border: `border-yellow-500/40`; Text: `text-yellow-400`
- done — Border: `border-green-500/40`; Text: `text-green-400`
- declined — Border: `border-fl-error/30`; Text: `text-fl-error-fg`

### `/admin/feedback` (`frontend/src/app/(app)/admin/feedback/page.tsx`)

Paginated feedback queue for admins, showing 10 entries per page. Filters: `q` search, type (all/feature/bug), status, and sort (date/votes). Entries with `status=done` are hidden from the default queue and only appear when the Done status filter is selected. The page uses shared admin primitives (`AdminPageHeader`, `AdminPanel`, `AdminMetric`, `AdminBadge`) and renders a dense desktop table plus responsive mobile cards. Administrator authors use the same `AdminAuthorBadge` as the community board in both desktop and mobile layouts. Status changes use an inline `<select>` and trigger `PATCH /{id}/status`; delete uses `ConfirmDialog`. The page includes the shared `AdminNav` navigation alongside `/admin` and `/admin/users`.

---

## Navigation

- `/feedback` added to `bottomNavItems` in `frontend/src/app/(app)/layout.tsx` (alongside Settings and FAQ).
- The Feedback nav item shows a fixed circular red unread badge in desktop and mobile menus when `GET /api/feedback/unread-summary` returns a non-zero count. The display caps at `99+`. The feedback list also shows per-item unread labels beside status badges.
- `/feedback` added to `PROTECTED_ROUTES` in `frontend/src/middleware.ts`.
- `/admin/feedback` is protected by the `/admin` prefix already in `PROTECTED_ROUTES`.

---

## i18n

`feedback` namespace (45 keys) added to all 10 locale files: `en`, `es`, `fr`, `de`, `it`, `nl`, `pl`, `pt`, `ro`, `ru`. `nav.feedback` key added to all 10 locales. Admin feedback queue labels live in the `admin` namespace. All non-English locales have full native translations for UI strings, status labels, and unread labels.

---

## Admin email notifications

When a user creates a new feature request or bug report, an email is sent to `CONTACT_EMAIL` (if `EMAIL_ENABLED=true` and `CONTACT_EMAIL` is configured).

- **Triggered by:** `POST /api/feedback` only. Comments (`POST /{id}/comments`) do **not** send notifications.
- **Comment activity:** comments update the in-app unread counter for other users instead of sending email.
- **Language:** native language of the first admin user by ascending `id`, with English fallback for unsupported locales.
- **Subject:** localized equivalent of `[Feature Request] <title>` or `[Bug Report] <title>`.
- **Template:** `backend/app/templates/email/feedback_submitted.html` — shows type badge, author username, title, description, and a link to the admin feedback queue at `APP_BASE_URL/admin/feedback`.
- **Implementation:** `email_service.send_feedback_notification()`. Called via `asyncio.create_task()` after `db.commit()` to avoid blocking the HTTP response. Errors are logged but never re-raised — the entry is already persisted.
- **Config:** reuses existing `EMAIL_ENABLED` and `CONTACT_EMAIL` settings; no new env vars required.
