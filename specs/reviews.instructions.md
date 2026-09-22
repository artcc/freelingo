---
description: "Current-state specification for user product reviews: ownership, snapshots, moderation, public publication, review prompts, Settings management, landing carousel, and notifications."
applyTo: "backend/app/models/review.py, backend/app/schemas/review.py, backend/app/services/{review_service,email_service}.py, backend/app/routers/reviews.py, frontend/src/lib/{reviews,review-prompt-triggers}.ts, frontend/src/components/reviews/**, frontend/src/components/settings/ReviewSection.tsx, frontend/src/app/(app)/admin/reviews/**, frontend/src/app/page.tsx, messages/*.json"
---

# User Reviews

## Purpose

Authenticated active users can submit a product rating and optional comment. Administrators moderate
reviews before positive reviews become public social proof on the landing page.

The API does not require email verification, subscription, a study plan, or completed learning
activity. An administrator can also create a personal review through the user endpoints.

## Data model

`reviews` stores:

- `user_id`: required, unique owner with `ON DELETE CASCADE`.
- `user_display_name`: snapshot refreshed when the user edits the review.
- `target_language`: active-language snapshot refreshed on edit.
- `rating`: required integer from 1 to 5, enforced by schema and database check.
- `comment`: optional text, limited to 2000 characters by schema.
- `is_approved`: moderation flag, false by default.
- `created_at`: stable original creation timestamp.
- `updated_at`: changed on user edits and moderation.

The unique user ID permits one existing review per user. Deleting that row allows the user to create
a new review later.

Target language is derived server-side from the active `UserLanguage`, with the user's compatibility
`target_language` as fallback. The snapshot does not update when profile or language changes unless
the review itself is edited.

Comments are trimmed before persistence; empty or whitespace-only content becomes null.

## User API

All user operations require authentication but no subscription, freemium, or maintenance access.

### `GET /api/reviews/me`

- Rate limit: `60/minute`.
- Always returns a state object for an authenticated user.
- Without a review: `has_review=false`, `review=null`.
- With a review: returns the full owner/admin representation, including approval state.

### `POST /api/reviews`

- Rate limit: `5/hour`.
- Requires rating; comment is optional.
- Creates snapshot fields server-side and starts unapproved.
- Returns `201`.
- Duplicate prevention uses a pre-check and the database unique constraint.
- An existing review returns `409 review_already_exists`.
- Successful creation schedules a best-effort administrator email.

### `PATCH /api/reviews/me`

- Rate limit: `10/hour`.
- Requires rating, so this is a full review-content update rather than a sparse patch.
- Omitting comment removes it.
- Refreshes name/language snapshots and `updated_at`.
- Always resets approval to false, including an identical edit.
- Missing review returns `404 review_not_found`.

### `DELETE /api/reviews/me`

- Rate limit: `10/hour`.
- Permanently removes the current user's review and returns `204`.
- Missing review returns `404 review_not_found`.

## Moderation API

Every administrative endpoint requires `role=admin` and is limited to `60/minute`.

`GET /api/admin/reviews` supports:

- optional approval, rating, and target-language filters;
- ascending or descending creation order;
- `skip >= 0`;
- `1 <= limit <= 100`, defaulting to 10;
- a filtered total before pagination.

Ordering uses creation time without an ID tie-breaker, so equal timestamps do not have a guaranteed
relative order.

`PATCH /api/admin/reviews/{review_id}` changes only `is_approved`. Administrators may approve any
rating, but approval below four stars does not make it public. Missing IDs return
`404 review_not_found`.

`DELETE /api/admin/reviews/{review_id}` permanently removes any review and returns `204` or the same
not-found error. Administrators cannot edit rating, comment, or snapshots.

## Public API

`GET /api/reviews/public`:

- requires no authentication;
- rate limit: `60/minute`;
- returns only `is_approved=true` and `rating >= 4`;
- orders by creation time descending without an ID tie-breaker;
- accepts only `limit` from 1 to 100, defaulting to 100;
- has no offset, cursor, total, or language filter;
- omits user ID, approval state, and update time.

The endpoint's maximum collection is the public carousel dataset, not a paginated representation of
all approved reviews.

## Review prompt

`ReviewForm` is shared by automatic prompts and Settings. It provides an accessible 1-5-star radio
group, optional comment, submit state, and generic localized errors. Rating is required; comment is
not.

When the prompt opens, it requests `/api/reviews/me`:

- an existing review suppresses the prompt;
- a successful no-review response shows the form;
- a failed lookup shows an error-only state and prevents submission.

Closing or cancelling never creates a review. It records client-only dismissal state under
`freelingo:reviewPromptDismissed`:

- 14-day cooldown from the latest dismissal;
- maximum three dismissals;
- global to the browser origin, not user, language, or trigger;
- malformed or absent data falls back to no dismissals.

Closing the error state also counts. Read access to local storage is guarded; a storage write failure
can currently prevent the close callback. The prompt does not provide explicit dialog semantics,
Escape handling, or backdrop-close behavior.

## Prompt triggers

The application may ask after these successful moments:

- Voice: the user manually stops a WebSocket session that has been live for at least five minutes.
  Timeout, error, remote close, and route unload do not trigger it.
- Lesson: completion advances from the completed unit to another unit or completes the plan. Failure
  to determine the next unit suppresses the prompt unless the plan is complete. The plan counts as
  complete when the `/today` `completion` state is `ready` or `taken`; a plan whose state is
  `in_progress` never counts as complete. Without a `completion` field, a `progress_day` at
  `total_days` is the legacy fallback.
- Reading: a successful new attempt submission.
- Listening: a successful new attempt submission.

Reading and Listening replay never trigger the prompt. No score threshold applies. Every trigger
uses the shared cooldown and maximum-dismissal rules; the backend uniqueness constraint remains the
final duplicate guard.

## Settings

The Community section in Settings loads `/api/reviews/me`.

- No review: empty form creates with POST.
- Existing review: prefilled form updates with PATCH.
- Unapproved review: pending-moderation hint.
- Successful save or delete: short confirmation.
- Delete: confirmation dialog before the request.
- Initial load failure: error state without the form or an explicit retry control.

## Administrative frontend

`/admin/reviews` uses ten-item pages and supports approval-state and rating filters. Backend language
and order filters are not exposed by this page. It shows snapshot name, status, stars, English
language name, browser-locale date, and comment/fallback.

Administrators can approve, unapprove, and delete with confirmation. After mutation, the page reloads
the effective page so filters and page bounds remain valid. Backend authorization protects every
administrative request.

## Landing carousel

The server-rendered landing requests `/api/reviews/public?limit=100` with five-minute revalidation.
Failure is non-fatal and hides both the section and its navigation link.

The carousel displays:

- snapshot display name;
- localized target-language name;
- accessible five-star rating;
- comment or localized neutral fallback;
- six-line comment clamp;
- responsive horizontal snap scrolling;
- manual scroll and automatic 320-pixel advance every 3.5 seconds;
- wrap to the beginning at the end.

One review is centered without auto-scroll. Average rating and count describe only the returned
maximum-100 collection, not necessarily every review in the database.

## Email notification

Creation, but not editing, schedules `send_review_notification()` after commit. It sends only when
email and `CONTACT_EMAIL` are configured. Locale comes from the first administrator's native
language, with English fallback.

The template includes escaped name, rating, language code, optional comment, and an admin-review
link. Delivery errors are logged and never roll back or alter the review response.

## Related specifications

- `api-endpoints.instructions.md` — endpoint inventory.
- `database-models.instructions.md` — complete model definition.
- `voice-conversation.instructions.md` — voice trigger lifecycle.
- `listening.instructions.md` and `reading.instructions.md` — exercise triggers and replay behavior.
