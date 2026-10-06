---
description: "Current-state specification for optional Stripe billing, subscription status, freemium trial and quotas, paywalls, maintenance mode, administrative visibility, and post-assessment voice access."
applyTo: "backend/app/core/{config,deps}.py, backend/app/models/user.py, backend/app/services/{subscription_service,freemium_service,assessment_voice_trial}.py, backend/app/routers/{billing,freemium,config,admin,conversation}.py, frontend/src/store/{config,freemium,auth}.ts, frontend/src/components/billing/**, frontend/src/components/MaintenanceGate.tsx, frontend/src/app/(auth)/billing/**, frontend/src/app/(app)/{chat,conversation,listening,reading,lesson,settings,dashboard}/**, frontend/src/app/page.tsx, docker-compose*.yml, .env.example"
---

# Subscriptions and Freemium

## Purpose and runtime toggle

FreeLingo optionally combines Stripe subscriptions with limited freemium access. `STRIPE_ENABLED`
defaults to `false` and is the principal runtime switch.

With Stripe disabled:

- `is_subscribed()` grants full feature access regardless of stored status;
- the billing router is not registered;
- freemium checks and usage recording are bypassed;
- pricing, billing, subscription status, and subscription filters are hidden in the frontend;
- quota administration remains available.

With Stripe enabled, only `active` and `trialing` statuses provide unlimited subscription access.
Other statuses can still use an active freemium trial or available feature quota.

## Persisted subscription state

Subscription fields are global user settings:

- `stripe_customer_id` and `stripe_subscription_id`;
- `subscription_status`;
- `subscription_ends_at`;
- `cancel_at_period_end`;
- `trial_used` for the Stripe card trial;
- `freemium_trial_ends_at` and `freemium_trial_used`;
- `assessment_voice_trial_used`.

Recognized Stripe states are `none`, `trialing`, `active`, `past_due`, `canceled`, `incomplete`,
`incomplete_expired`, `unpaid`, and `paused`. Database constraints do not enforce this set.

`subscription_ends_at` and `cancel_at_period_end` are presentation and lifecycle data; access remains
active while status is `active` or `trialing`. Revocation depends on synchronized Stripe status.
Administrators do not bypass subscription policy, although they do bypass maintenance mode.

## Configuration

Stripe configuration includes:

- secret and webhook keys;
- monthly and yearly Price IDs;
- Stripe trial days;
- `STRIPE_BASE_URL` for checkout and portal returns;
- current and original display prices for monthly and yearly plans.

The public config endpoint exposes presentation-safe toggles, trial length, display prices, TTS
metadata, and maintenance state. It never exposes Stripe secrets or Price IDs.

The application does not perform a complete startup validation of Stripe configuration. Checkout
returns `503` when the selected Price ID is absent.

## Access policies

The consuming-feature dependency follows:

1. Stripe disabled: allow.
2. Status `active` or `trialing`: allow.
3. Active no-card freemium trial: allow.
4. Remaining feature quota: allow.
5. Otherwise: HTTP `402`.

The read-only variant follows the same first three steps but allows an exhausted quota when that
feature's configured limit is greater than zero. A zero limit means Premium-only and blocks read-only
access too.

Redis failure while checking freemium access fails closed with HTTP `402` and
`reason=freemium_unavailable`. A normal exhausted quota returns `reason=freemium_exhausted`, feature,
remaining, and limit.

Currently gated operations are:

- sending a chat message;
- completing a lesson;
- generating and submitting Listening attempts;
- generating and submitting Reading attempts;
- creating new Error Detective games (durable reservation policy below);
- voice-conversation warmup and WebSocket connection.

Read-only policy protects chat history, Listening next/audio/history, and Reading next/history.

Profile, Settings, assessment, plan generation, lesson viewing and answers, flashcards, progress,
grammar, vocabulary, phrasebook, direct TTS/STT, and manual memory management are not subscription
gated. Memory management is also not blocked by maintenance mode.

## Stripe Checkout

`POST /api/billing/checkout`:

- requires authentication and accepts `monthly` or `yearly`;
- rate limit: `60/minute`;
- selects the configured server-side Price ID;
- creates and persists a Stripe Customer when absent;
- creates a subscription Checkout Session with promotion codes enabled;
- records `user_id` in session and subscription metadata;
- includes a Stripe trial only when configured days are positive and `trial_used` is false;
- returns checkout success and cancellation to `STRIPE_BASE_URL`;
- returns the Stripe-hosted URL.

The endpoint does not currently prevent an already subscribed user from opening another checkout and
does not send an idempotency key.

`POST /api/billing/portal` requires authentication, has a `60/minute` limit, requires a stored
Customer ID, and returns a Stripe Customer Portal URL with Settings as the return target. It does not
require a currently active subscription.

## Stripe webhook

`POST /api/billing/webhook` is public at the network layer, limited to `200/minute`, and verifies the
Stripe signature over the raw body before processing. Invalid payload or signature returns `400`.
Processing failure rolls back and returns `500` so Stripe can retry. Unsupported events return 200.

Handled events:

- `checkout.session.completed`: finds the user by Customer or metadata, requires and retrieves the
  Stripe Subscription before granting access, stores identifiers/status/period, clears scheduled
  cancellation, marks a real trial as used, and applies default general quotas.
- `customer.subscription.updated`: binds a missing current subscription ID, ignores a different
  known subscription as stale, preserves the prior status when Stripe sends an unknown value, and
  synchronizes period and scheduled cancellation.
- `customer.subscription.deleted`: ignores stale subscriptions, marks current status canceled, and
  clears scheduled cancellation.
- `invoice.payment_failed`: accepts both historical and current Stripe invoice subscription shapes,
  ignores stale subscription IDs, and marks the current subscription past due.

Webhook event IDs are not persisted for idempotency. Activation quotas are applied by checkout
completion, not by a later transition received only through `subscription.updated`.

## Stripe card trial

Checkout includes `STRIPE_TRIAL_DAYS` only when the configured value is positive and `trial_used` is
false. Abandoning checkout does not consume the right. The flag is committed when verified checkout
completion reports `trialing`; direct `active` activation and administrative overrides do not mark it.

The Stripe card trial and the freemium no-card trial are independent. A Stripe `trialing` status has
subscription precedence and does not consume freemium counters.

## Freemium trial

When Stripe and `FREEMIUM_TRIAL_ENABLED` are active, eligible registration creates a no-card trial
ending after `FREEMIUM_TRIAL_DAYS` and marks it granted. Eligible older or admin-created users can
receive it best-effort when their profile is first loaded.

Trial activity depends on the runtime toggle and a future UTC expiration. `freemium_trial_used`
prevents regranting but is not the active-state check. Disabling the toggle suspends an existing
trial; re-enabling it restores access only if its stored expiry remains in the future.

Freemium trial access bypasses feature counters but not global token or voice conversation limits.

## Freemium quotas

Defaults are:

- Chat: 5 successful messages per UTC day.
- Lessons: 3 successful completions per UTC day.
- Listening: 3 successful attempts per ISO week.
- Reading: 3 successful attempts per ISO week.
- Voice: 5 elapsed conversation minutes per ISO week, stored as seconds.
- Games: 3 new games per UTC day, configured by `FREEMIUM_GAMES_DAILY`.

Freemium counters are global per user, not per learning language. Zero means blocked for that feature.
Daily keys expire at the next UTC midnight; weekly keys expire at the next Monday UTC.

Usage is recorded after successful work:

- Chat after completed response and persistence.
- Lessons after atomic completion/progress/competency commit.
- Listening and Reading after persisted attempts, including replay.
- Voice from elapsed session seconds during cleanup when freemium quota was the effective access path.

Already-completed lesson retries return before quota checking or consumption. Generating or loading a
Listening/Reading exercise does not consume quota.

Counter increment plus TTL assignment is atomic through Lua. Availability checking and later usage
recording are separate operations, so concurrent requests can be admitted from the same remaining
balance. Usage recording is best-effort and does not roll back completed product work when Redis
fails.

Games uses a separate durable PostgreSQL admission contract: under a user-row lock, generation
reserves availability and successful validated content consumes it in the same transaction. Failure
releases the slot; expired reservations do not count. The creation UTC day owns consumption. Consumed
admissions survive plan deletion. Subscription/trial/Stripe-disabled bypass rules remain the same.
Session reads, answers and abandonment require ownership but no additional quota, so admitted games
remain playable after exhaustion or subscription expiry. Games creation is maintenance-gated;
saved games remain accessible. `GET /api/freemium/status` includes `games_remaining` and `games_limit`.

`GET /api/freemium/status` requires authentication, is limited to `60/minute`, and returns trial
state plus remaining and configured limits for all six features. The route exists when Stripe is
disabled, although the policy is inactive and the frontend normally does not request it.

## General quotas and subscription activation

General conversation and LLM quotas apply independently of freemium:

- weekly sessions;
- daily and weekly minutes;
- monthly tokens;
- maximum conversation duration;
- inactivity timeout.

For these user quotas, zero means unlimited. Verified checkout activation resets them from the
configured defaults. Administrators may override them regardless of Stripe state.

## Post-assessment voice demo

The one-time voice demo is available only with Stripe enabled to an unsubscribed user whose durable
demo right is unused. Its Redis credential lasts 24 hours, can be regenerated while unused, and
defaults to a five-minute session duration.

Voice access gives precedence to subscription, freemium trial, and remaining freemium voice balance
before considering the demo. Consequently, a supplied demo token is not consumed while an earlier
access path succeeds. When selected, the WebSocket deletes the token and marks the durable right used
as the session begins.

The demo does not grant access to chat, Listening, or Reading and remains subject to the user's
general token, session, and minute limits. Its stored plan/language metadata does not currently force
the WebSocket session context.

## Maintenance mode

Maintenance is a Redis runtime flag managed from Admin > System and exposed through public config.
It blocks chat, voice conversation, Listening, and Reading for non-admin users with HTTP `503` or
WebSocket close 1013. Administrators bypass maintenance. Other learning areas remain available.

Redis failure while checking maintenance is fail-open. Maintenance is checked when requests or
WebSocket sessions start; changing the flag does not terminate existing sessions. Frontend gates
replace the affected pages, but open clients do not receive push updates when the flag changes.

## Administration

Administrative APIs expose subscription fields and accept subscription filtering and recognized
status overrides. Moving a user from non-premium to `active` or `trialing` applies default quotas;
setting `none` clears the end date. Overrides update local access only and do not modify Stripe.

With Stripe disabled, frontend administration:

- hides active/trialing metrics and past-due alerts;
- hides and ignores subscription filters and values in the user list;
- hides subscription details and override controls;
- preserves quota controls.

Backend admin responses and update capabilities still include Stripe fields regardless of the
frontend toggle. The UI's monthly/yearly override maps locally to active access plus an approximate
30/365-day date; the actual billing interval is not persisted on the user.

## Frontend behavior

The config store loads public runtime flags. The freemium store caches status for 60 seconds and
provides optimistic decrement for chat, Listening, and Reading. Lessons refresh authoritative status
after completion; voice refreshes after session end.

`FreemiumQuotaBanner` shows active-trial time, remaining/limit values, Premium-only state for zero
limits, and low-balance emphasis. `PaywallBanner` renders inline upgrade or payment-recovery actions.
There is no `PaywallGate`; each feature page adapts only the consuming controls while preserving
readable history where backend policy permits.

`past_due`, `unpaid`, and `paused` use Customer Portal recovery. `none`, `incomplete`,
`incomplete_expired`, and `canceled` offer monthly/yearly checkout.

Landing pricing exists only when Stripe is enabled and the visitor is not known to be subscribed.
Anonymous plan selection is carried through registration; authenticated users can start checkout
directly. Billing success refreshes authentication and polls profile state before claiming Premium
or redirecting. Billing cancellation never claims a charge occurred.

The frontend is advisory: stale config or freemium state may temporarily present an action the
backend rejects. Backend dependencies remain authoritative.

## Related specifications

- `voice-conversation.instructions.md` — voice access and demo consumption.
- `listening.instructions.md` — Listening quota-consumption behavior.
- `reading.instructions.md` — Reading quota-consumption behavior.
- `api-endpoints.instructions.md` — endpoint request and response details.
- `database-models.instructions.md` — user subscription fields.
- `docker.instructions.md` — environment propagation.
