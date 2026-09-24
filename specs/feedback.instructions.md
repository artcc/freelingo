---
description: "Current-state specification for the authenticated feedback board: feature requests, bug reports, votes, comments, read state, moderation, pagination, notifications, and frontend behavior."
applyTo: "backend/app/models/feedback.py, backend/app/schemas/feedback.py, backend/app/routers/feedback.py, backend/app/services/email_service.py, frontend/src/app/(app)/feedback/**, frontend/src/app/(app)/admin/feedback/**, frontend/src/app/(app)/layout.tsx, frontend/src/components/admin/**, messages/*.json"
---

# Feedback

## Purpose

Feedback is an authenticated community board for feature requests and bug reports. Users can create
entries, discuss them in flat comment threads, and vote on feature requests. Administrators manage
entry status and may delete any entry or comment.

The application tracks unread activity per user and identifies administrator-authored entries and
comments with an `ADMIN` badge.

## Data model

### Entries

`feedback_entries` stores:

- `type`: `feature` or `bug` as validated by the API.
- `title`: 1-200 characters before router trimming.
- `description`: 1-5000 characters before router trimming.
- `status`: `pending`, `planned`, `in_progress`, `done`, or `declined`.
- `author_id`: required user owner with `ON DELETE CASCADE`.
- `vote_count`: denormalized counter starting at zero.
- `created_at`: UTC timestamp used for ordering.

New entries always start as `pending`. The database does not enforce type, status, text lengths, or a
non-negative vote count; those domains are maintained by request validation and router behavior.

### Votes

`feedback_votes` records one vote per `(entry_id, user_id)`, enforced by
`uq_feedback_vote`. Entry and user deletion cascade to votes. Only feature requests are voteable;
the router rejects votes on bugs.

### Comments

`feedback_comments` stores a flat comment body of 1-2000 characters before trimming, its entry,
author, and creation time. There are no replies, edits, moderation state, or per-comment pagination.

### Read state

`feedback_read_states` stores `last_read_at` for one `(entry_id, user_id)`, enforced by
`uq_feedback_read_state`. Entry and user deletion cascade to read markers.

## API representations

An embedded author exposes ID, username, display name, and current role. Entry responses include
`voted_by_me`, `unread_by_me`, and `comment_count`. Detail adds the complete ordered comment list.

The API does not provide entry-edit or comment-edit operations.

## Listing and pagination

`GET /api/feedback` requires authentication and is limited to `60/minute`.

It supports:

- `type=feature|bug`;
- `status=pending|planned|in_progress|done|declined`;
- `q`, up to 100 characters, across title, description, username, and display name;
- `sort=votes|date`;
- `order=asc|desc`;
- `skip >= 0` and `1 <= limit <= 100`, defaulting to 0 and 10.

Without an explicit status, entries marked `done` are excluded. The filtered total is calculated
before pagination. Ordering uses vote count or creation time plus entry ID in the same direction,
making offset pages deterministic when primary values tie.

The authenticated community and administrative pages use ten entries per page. The community view
defaults to feature requests sorted by votes; the admin queue defaults to date order.

## Entry lifecycle

`POST /api/feedback`:

- requires authentication and is limited to `10/hour`;
- trims title and description after schema validation;
- creates a pending entry with zero votes;
- marks the thread read for its author;
- returns HTTP `201`;
- schedules a best-effort administrator email after commit.

`GET /api/feedback/{id}` returns the enriched entry and all comments. It does not mark the thread
read automatically.

`DELETE /api/feedback/{id}` is limited to `60/minute`. The author or an administrator may delete an
entry; others receive `403 forbidden`. Deletion returns `204` and cascades to votes, comments, and
read states.

The schemas validate length before trimming. Consequently, whitespace-only title, description, or
comment input can currently pass length validation and be stored as an empty trimmed value.

## Voting

`POST /api/feedback/{id}/vote` requires authentication and is limited to `60/minute`.

- Feature votes toggle on and off.
- Adding creates the unique vote and increments `vote_count`.
- Removing deletes it and decrements the counter with a local zero floor.
- Users may vote on their own feature requests and on features in any status.
- Voting on a bug returns `400 only_features_are_voteable`.

Vote-row uniqueness is database-enforced, but counter updates and toggle decisions are not one SQL
atomic expression. Concurrent toggles can conflict or desynchronize the denormalized counter.

## Comments

- `GET /api/feedback/{id}/comments`: authenticated, `60/minute`; returns all comments oldest-first
  and their total.
- `POST /api/feedback/{id}/comments`: authenticated, `20/hour`; creates a comment, marks the thread
  read for that author, and returns `201`.
- `DELETE /api/feedback/{id}/comments/{comment_id}`: authenticated, `60/minute`; verifies that the
  comment belongs to the path entry and allows deletion by its author or an administrator.

Users may comment on any existing entry regardless of type or status. Comment ordering uses creation
time without an ID tie-breaker.

## Status moderation

`PATCH /api/feedback/{id}/status` is limited to `60/minute` and requires an administrator. It accepts
only the five supported statuses and returns the updated entry.

The administrative queue uses the same authenticated listing endpoint as the community board. The
backend applies administrator authorization to status changes and privileged deletion, but not to
reading the list itself. The frontend admin route does not add a separate role check beyond normal
protected-route handling.

The admin page supports search, type, status, and sort controls, plus inline status changes and
confirmed entry deletion. Although the backend allows administrators to delete any comment, the
community comment UI currently renders deletion only for the comment author.

## Unread behavior

Unread state counts feedback threads, not individual entries plus comments.

A thread is unread when:

- another user created it after the learner's marker, or no marker exists; or
- another user added a comment after the marker.

The user's own entry and comments do not create unread activity for that user. Votes and status
changes do not count. Entries in `done` or `declined` can still contribute to the summary; a `done`
entry may therefore count while hidden by the default list filter.

- `GET /api/feedback/unread-summary`: authenticated, `60/minute`; returns unread thread count.
- `POST /api/feedback/{id}/read`: authenticated, `60/minute`; creates or updates only that thread's
  marker.

Opening detail in the frontend calls the read endpoint, updates the local entry, and emits a browser
event so the layout reloads its badge. There is no polling, push update, or cross-client real-time
synchronization. The navigation badge caps presentation at `99+`.

Read-marker upsert is implemented as lookup followed by insert/update and is not specifically
serialized for simultaneous first reads.

## Notifications

Creating an entry schedules `send_feedback_notification()` after database commit. It sends to
`CONTACT_EMAIL` only when email is enabled and configured. The message uses the native language of
the first administrator by ascending ID, with English fallback, and links to `/admin/feedback`.

Email errors are logged without changing the successful creation response. Comments do not send
email; they rely on unread state.

## Frontend behavior

The community page uses local state and provides:

- feature and bug tabs;
- status filtering and vote/date sorting;
- modal creation;
- deterministic pagination;
- inline feature voting;
- detail with description and flat comments;
- confirmed entry and comment deletion where the UI exposes permission;
- red unread labels beside entry status;
- the shared `AdminAuthorBadge` for live administrator roles.

There is no community search control even though the API supports `q`. The detail view reuses the
selected list item and loads comments separately rather than requesting the detail endpoint.

The frontend has no dedicated Feedback store. It uses authenticated `apiFetch` and component-local
state. There is no request identity or cancellation between filter loads, so a late older response
can replace newer list state. Some mutations are optimistically reflected without consistently
checking non-success responses.

Feedback UI, status/read labels, and administrator author badges use the active interface locale.
Croatian comment counts use ICU plural categories, including the singular form for counts such as
21 and 31 and the appropriate forms for `few` and `other`.
The vote HTML tooltip remains a fixed label.

## Related specifications

- `api-endpoints.instructions.md` — endpoint inventory.
- `database-models.instructions.md` — complete table definitions.
- `architecture-frontend.instructions.md` — authenticated and administrative page structure.
