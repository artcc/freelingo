---
description: "Current SlowAPI rate-limit integration, client-key behavior, endpoint limit classes, WebSocket protections, and 429 contract."
applyTo: "backend/app/main.py, backend/app/core/{config,limiter}.py, backend/app/routers/**/*.py"
---

# Rate Limiting

## Integration

FreeLingo uses SlowAPI with Redis storage from `REDIS_URL`. `RATE_LIMIT_ENABLED` enables or disables
enforcement. The limiter object and standard SlowAPI exception handler are registered on the FastAPI
application.

The limiter configures `60/minute` as its default, but the application does not install
`SlowAPIMiddleware`. Every HTTP endpoint therefore carries an explicit `@limiter.limit(...)`
decorator; adding an undecorated endpoint is not an accepted way to inherit protection.

`api-endpoints.instructions.md` owns endpoint request/response contracts. This document is the
canonical reference for limit values.

## Client key

All limits are IP-based. `_get_real_ip` resolves the key in this order:

1. `X-Real-IP`.
2. First address in `X-Forwarded-For`.
3. Socket client host.

The production reverse proxy must replace trusted forwarding headers rather than accept arbitrary
client values. Authenticated users behind one IP share buckets, and one user moving between IPs uses
different buckets.

## Standard limit

Unless listed below as an exception, current REST endpoints use an explicit `60/minute` decorator.
This includes ordinary reads, profile changes, language management, progress, resource retrieval,
flashcard CRUD/review, admin operations, memories, feedback reads/mutations, and review reads/deletes.

## Authentication and destructive operations

- `POST /api/auth/register`: `5/minute`.
- `POST /api/auth/login`: `10/minute`.
- `POST /api/auth/resend-verification`: `3/minute`.
- `POST /api/auth/forgot-password`: `5/minute`.
- `POST /api/auth/reset-password`: `5/minute`.
- `DELETE /api/auth/me`: `5/minute`.
- `DELETE /api/admin/users/{user_id}`: `5/minute`.
- `DELETE /api/languages/{target_language}`: `5/minute`.

## Generated and evaluated learning operations

- `GET /api/assessment/start`: `10/minute`.
- `POST /api/assessment/submit`: `10/minute`.
- `POST /api/assessment/free-write`: `10/minute`.
- `POST /api/assessment/complete`: `10/minute`.
- `POST /api/assessment/voice-trial`: `10/minute`.
- `GET /api/assessment/level-test/questions/{plan_id}`: `5/minute`.
- `POST /api/assessment/level-test/submit`: `10/minute`.
- `POST /api/study-plan/generate`: `10/minute`.
- `GET /api/study-plan/today`: `20/minute`.
- `POST /api/lessons/exercises/{exercise_id}/answer`: `20/minute`.
- `POST /api/lessons/exercises/{exercise_id}/regenerate`: `5/hour`.
- Lesson/exercise native explanation or hint generation: `10/minute`.
- Grammar, Vocabulary, or Phrasebook native-help generation: `10/minute`.
- `GET /api/phrasebook/audio/{category_id}/{phrase_index}`: `30/minute`.
- `POST /api/flashcards/generate`: `20/minute`.
- `POST /api/flashcards/from-word`: `30/minute`.
- `POST /api/chat`: `30/minute`.
- `POST /api/conversation/warmup`: `20/minute`.
- `POST /api/tts`: `20/minute`.
- `POST /api/stt`: `20/minute`.

## Games

- `GET /api/games/{game_type}` and `GET /api/games/sessions/{id}`: `60/minute`.
- `POST /api/games/{game_type}`: `5/minute`.
- `POST /api/games/sessions/{id}/answer`: `60/minute` for Detective steps or Sentence Order submissions.
- `POST /api/games/sessions/{id}/abandon`: `10/minute`.

`game_type` accepts `detective` and `sentence-order` through shared catalog/start handlers.
Generation polling is non-overlapping, normally every five seconds, with bounded transport recovery.
Rate limiting is independent of the global per-user daily game admission quota.

## Listening and Reading

Both domains use:

- `GET /api/{domain}/next`: `60/minute`.
- `POST /api/{domain}/generate`: `5/minute`.
- `POST /api/{domain}/attempt`: `20/minute`.
- history and Listening audio retrieval: `60/minute`.

Generation status uses immediate `/next` responses and non-overlapping client queries every ten
seconds. The read budget allows this cadence with headroom for shared IPs. Clients back off on 429
and honor `Retry-After` when present; generation itself remains limited to `5/minute`.

## Community, contact, and billing

- `POST /api/contact`: `5/hour`.
- `POST /api/feedback`: `10/hour`.
- `POST /api/feedback/{entry_id}/comments`: `20/hour`.
- `POST /api/reviews`: `5/hour`.
- `PATCH /api/reviews/me`: `10/hour`.
- `DELETE /api/reviews/me`: `10/hour`.
- `POST /api/admin/dashboard-banner/translate`: `10/minute`.
- `POST /api/billing/webhook`: `200/minute`.

## WebSocket

`/ws/conversation` is not decorated by SlowAPI. It is constrained by first-message JWT validation,
subscription/freemium and maintenance policy, global voice quotas, maximum session duration, and
inactivity timeout. These controls are not equivalent to a connection-attempt IP rate limit.

## 429 response

SlowAPI's registered standard handler returns HTTP 429 with its standard error body. The application
does not define a custom `detail` schema or guarantee `Retry-After`/rate-limit headers. Frontend token
refresh must remain limited to 401 and must not run for 429.

## Operational rule

Disable rate limiting only for trusted private/development environments. Changes to decorators or
limit values must update this spec and the affected endpoint documentation together.
