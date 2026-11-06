---
description: "Current-state specification for Stripe billing, optional RevenueCat entitlement synchronization, freemium access, paywalls, maintenance, and subscription administration."
applyTo: "backend/app/core/{config,deps}.py, backend/app/models/{user,billing_webhook,billing_checkout}.py, backend/app/services/{subscription_service,revenuecat_service,stripe_checkout_service,freemium_service,assessment_voice_trial}.py, backend/app/routers/{billing,revenuecat,freemium,config,admin,conversation}.py, backend/app/schemas/revenuecat.py, frontend/src/store/{config,freemium,auth}.ts, frontend/src/components/billing/**, frontend/src/components/MaintenanceGate.tsx, frontend/src/app/(auth)/billing/**, frontend/src/app/(app)/{chat,conversation,listening,reading,lesson,settings,dashboard}/**, frontend/src/app/page.tsx, docker-compose*.yml, .env.example"
---

# Subscriptions and Freemium

## Purpose and runtime toggle

FreeLingo optionally combines Stripe subscriptions with limited freemium access. `STRIPE_ENABLED`
defaults to `false` and is the principal runtime switch.

`REVENUECAT_ENABLED` defaults to `false` and only applies when Stripe is enabled. When enabled,
RevenueCat is the authority for the shared Premium entitlement; Stripe still handles web Checkout,
Customer identities, and its Customer Portal. No store-specific subscription model is required for
access authorization. Both providers use the same global FreeLingo account identity.

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
- `revenuecat_synced_at`, nullable until the first verified RevenueCat synchronization;
- `trial_used` for the Stripe card trial;
- `freemium_trial_ends_at` and `freemium_trial_used`;
- `assessment_voice_trial_used`.

Recognized Stripe states are `none`, `trialing`, `active`, `past_due`, `canceled`, `incomplete`,
`incomplete_expired`, `unpaid`, and `paused`. Database constraints do not enforce this set.

`subscription_ends_at` and `cancel_at_period_end` are presentation and lifecycle data; access remains
active while the persisted status is `active` or `trialing`. In Stripe-only mode, revocation depends on
synchronized Stripe status. In RevenueCat mode, the last confirmed snapshot remains authoritative
until a successful reconciliation changes it. A cached period end passing does not revoke access:
Stripe renewal notifications can arrive after RevenueCat has extended the entitlement. Provider
failures neither revoke confirmed Premium nor grant it to an unsubscribed account. Access checks,
public profiles, and admin reporting use the same persisted status. A null expiration in a verified
RevenueCat entitlement represents lifetime access.
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

RevenueCat configuration, required only when both billing flags are enabled:

- `REVENUECAT_API_KEY`: backend-only secret key for API v1 customer reads;
- `REVENUECAT_WEBHOOK_AUTHORIZATION`: exact, high-entropy Authorization header configured at RevenueCat;
- `REVENUECAT_ENTITLEMENT_ID`: entitlement identifier, default `premium`;
- `REVENUECAT_ENVIRONMENT`: `PRODUCTION` (default) or `SANDBOX`;
- `REVENUECAT_STRIPE_PUBLIC_API_KEY`: optional RevenueCat Stripe-app public key for explicit receipt imports.

Startup rejects missing required RevenueCat values. Keys and webhook credentials are never returned
by public configuration. Production and sandbox deployments use separate RevenueCat projects to keep
API v1's aggregated customer entitlements isolated.

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
- creating new Error Detective, Sentence Order, or Vocabulary Pairs games (durable reservation policy below);
- voice-conversation warmup and WebSocket connection.

Read-only policy protects chat history, Listening next/audio/history, and Reading next/history.

Profile, Settings, assessment, plan generation, lesson viewing and answers, flashcards, progress,
grammar, vocabulary, phrasebook, direct TTS/STT, and manual memory management are not subscription
gated. Memory management is also not blocked by maintenance mode.

## Stripe Checkout

`POST /api/billing/checkout`:

- requires authentication and accepts `monthly` or `yearly`;
- reconciles the account with RevenueCat first when enabled; provider failure returns `503`;
- rejects an already-subscribed account with `409 subscription_already_active`;
- rate limit: `60/minute`;
- selects the configured server-side Price ID;
- creates and persists a Stripe Customer when absent, using a durable customer-creation request and key;
- creates a subscription Checkout Session with promotion codes enabled and a one-hour expiry;
- records `user_id` in session and subscription metadata;
- includes a Stripe trial only when configured days are positive and `trial_used` is false;
- returns checkout success and cancellation to `STRIPE_BASE_URL`;
- returns the Stripe-hosted URL; an existing recoverable Stripe subscription returns a Customer Portal
  URL instead of opening another purchase.

`stripe_checkout_service.py` serializes creation on the user row and persists one `billing_checkouts`
reservation per user before contacting Checkout. The reservation freezes the complete session request
and its UUID idempotency key. Workers reacquire the user lock and reload the reservation after a commit.
When the account has no Stripe Customer, a preliminary reservation freezes the Customer's email, name,
and identity metadata before the first provider call. Retries reuse those original parameters even if
the profile changes. The Customer key is namespaced separately from session keys. The Customer ID and
deletion of that preliminary reservation commit together before subsequent provider operations; the
normal session reservation is then prepared using the persisted Customer. Existing session reservations
remain compatible without Customer request data.
The same price reuses the open session; changing prices expires it before creating a replacement.
Completed sessions are checked against their current Stripe Subscription, including before webhooks
arrive. Sessions opened before reservations existed are expired before a new reservation is created.
If payment races expiration, the request fails without issuing another session.

When a session ID is unknown, recovery first paginates the customer's sessions and matches the
reservation metadata. It does not filter by a locally inferred creation time because provider clocks
can differ. A recovered session is retrieved for its current state. If no match exists and the
reservation remains unexpired, creation retries the persisted key and parameters, then retrieves
current state rather than trusting a replayed creation response. Stripe requires at least 30 minutes
until expiry for a newly created session: its definitive `expires_at` validation rejection permits
renewing a reservation with no discovered result. Other validation errors, in-flight requests, timeouts,
and server errors do not authorize replacement. Once the reservation deadline passes, the old key is
never resubmitted because Stripe may have pruned it. Provider errors return `503` and preserve the
committed reservation; failed discovery also fails closed.

Before returning an open Checkout or reserving a new one, the service checks the customer's Stripe
subscriptions with pagination. `active`/`trialing` subscriptions block another purchase with `409`.
An open session can resume its own `incomplete` subscription's initial payment; any other incomplete
subscription, or a completed session with a still-incomplete payment, returns
`409 subscription_payment_pending`. `past_due`, `unpaid`, and `paused` route to
Customer Portal. Terminal `canceled`/`incomplete_expired` subscriptions permit a new purchase. These
checks decide billing navigation, not Premium access: in RevenueCat mode only RevenueCat updates
the entitlement snapshot. Verified historical Stripe trial usage suppresses a second card trial.

`POST /api/billing/portal` requires authentication and has a `60/minute` limit. In RevenueCat mode it
first reads the customer's HTTPS `management_url`, allowing the existing web button to manage the
subscription where it was purchased. Without a provider management URL, it requires a stored Stripe
Customer ID and returns a Stripe Customer Portal URL with Settings as the return target. It does not
require a currently active subscription. If RevenueCat fails or returns invalid data or an unsafe URL,
the endpoint falls back to the authenticated user's stored Stripe Customer ID; without one it returns
`503`. A successful RevenueCat read with no management URL and no Stripe Customer ID returns `400`.
Stripe portal creation uses the asynchronous SDK; Stripe failures return a sanitized `503` without
changing the stored billing identity or access snapshot.

## Stripe webhook

`POST /api/billing/webhook` is public at the network layer, limited to `200/minute`, and verifies the
Stripe signature over the raw body before processing. Invalid payload or signature returns `400`.
Processing failure rolls back and returns `500` so Stripe can retry. Unsupported events return 200.

Handled events:

The state mutations below apply in Stripe-only mode. With RevenueCat enabled, Stripe notifications
only retain billing identifiers and the verified Stripe trial-used flag; they never overwrite shared
subscription status, expiration, cancellation state, or activation quotas. Both synchronization paths
lock the user row before modifying billing data.

- `checkout.session.completed`: finds the user by Customer or metadata and retrieves the current
  Stripe Subscription before applying identifiers/status/period/scheduled cancellation. Late sessions
  cannot rebind an account from a different persisted Customer or replace a current non-terminal
  subscription. Verified current or historical trial usage marks the card trial as used.
- `customer.subscription.updated`: binds a missing current subscription ID, ignores a different
  known subscription as stale, and retrieves the current Subscription rather than applying the event
  snapshot. Unknown provider statuses preserve the prior status.
- `customer.subscription.deleted`: ignores stale subscriptions and reconciles the current Subscription;
  a confirmed canceled status clears scheduled cancellation.
- `invoice.payment_failed`: accepts both historical and current Stripe invoice subscription shapes,
  ignores stale subscription IDs and one-off invoices, and reconciles the current Subscription. An old
  invoice failure cannot overwrite a subsequent payment recovery.

Stripe event IDs are persisted in `stripe_webhook_receipts` and commit atomically with account changes.
Duplicates do not repeat provider reads or reset quotas; failed processing rolls back the receipt so
delivery remains retryable. Provider reads happen under the user lock, avoiding stale event snapshots
and concurrent overwrites. Default activation quotas apply only on a non-Premium to Premium transition,
including a subscription update received before Checkout completion.

## RevenueCat synchronization

The canonical App User ID is `str(users.id)`. Stripe Checkout Session and Subscription metadata both
contain it as `user_id`; RevenueCat's Stripe integration reads that metadata field. Clients must use
the same authenticated account identity, not an email address or Stripe Customer ID. Anonymous aliases
are only useful when RevenueCat associates them with a known canonical ID.

### Customer profile attributes

When both billing flags are enabled, the backend publishes profile attributes using
`POST /v1/subscribers/{app_user_id}/attributes` and the backend-only `REVENUECAT_API_KEY`:

- `$displayName`: the persisted FreeLingo display name;
- `$email`: the persisted email, or an empty string to clear a previously stored email;
- `native_language`: the persisted native-language code;
- `country_estimate`: an ISO country code inferred by a fixed language-to-country convention;
- `country_estimate_source`: `native_language` when a mapping exists, otherwise empty.

The country estimate is reporting metadata, not verified residence, billing country, or RevenueCat's
built-in Country field. The convention is `en → GB`, `es → ES`, `fr → FR`, `pt → PT`, `de → DE`,
`it → IT`, `ru → RU`, `nl → NL`, `pl → PL`, `ro → RO`, `tr → TR`, `sv → SE`, `da → DK`, `fi → FI`,
and `hr → HR`. Unknown languages clear the estimate and its source instead of inventing a fallback.
RevenueCat's built-in Country is determined separately from transaction data or last-seen IP country.

Attributes are sent during Checkout's RevenueCat reconciliation, explicit self/admin synchronization,
and after successfully saving name, email, or native language through the profile endpoint. An admin
display-name update also sends the target user's current attributes. Existing users can be populated
through explicit synchronization. Profile reads, ordinary learning requests, and webhooks do not send
attributes. The helper reloads the persisted profile under the user-row lock and sends `updated_at_ms`
with each value so older provider writes cannot overwrite newer timestamped attributes.

Attribute requests have a three-second total deadline. Provider/configuration failures emit a sanitized
warning and do not roll back a saved profile, block Checkout, or change subscription access. A later
eligible action retries the current values; there is no background attribute retry job. Attribute
response bodies are not used as entitlement snapshots. These metadata fields never authorize access.

### Entitlement reconciliation

`POST /api/billing/revenuecat/webhook` verifies the configured Authorization header using a constant-time
comparison before parsing API v1 events. Dashboard `TEST` events and events explicitly belonging to
the other environment are acknowledged without changing access. Unknown/deleted account identities
are also acknowledged. Additional fields and new event types are accepted.

For identified accounts, the handler retrieves `GET /v1/subscribers/{app_user_id}` from RevenueCat;
webhook transaction fields are not themselves access grants or revocations. It resolves canonical IDs
from the current ID, original ID, aliases, both sides of transfers, and redemption identities. Transfers
reconcile all known affected accounts atomically, acquiring user-row locks in ascending ID order.

The configured entitlement determines the shared snapshot:

- absent entitlement: `none`;
- unexpired entitlement: `active`, or `trialing` for a trial period;
- expired entitlement: `canceled`, including expirations with a historical billing issue;
- cancellation detection sets `cancel_at_period_end` without revoking unexpired access;
- grace-period expiry extends the access deadline; a billing issue alone does not revoke access;
- a matched purchase must belong to the configured environment; mismatched or malformed snapshots fail
  without overwriting local access;
- a snapshot older than `revenuecat_synced_at` cannot overwrite a newer one.

An expired entitlement with `billing_issues_detected_at` does not establish that the store subscription
is recoverable. The UI offers subscription plans for the canceled state; Checkout verifies live Stripe
billing state and routes recoverable subscriptions to the portal instead of creating duplicate charges.

The event receipt, account snapshot, and activation quotas commit in one database transaction.
Duplicate event IDs are acknowledged without repeating provider reads or resetting quotas. Failed
requests roll back the receipt and account changes and return `503`, permitting delivery retries.
Quota defaults are applied only when the persisted state transitions from non-Premium to Premium.
Requests to RevenueCat have a ten-second overall deadline; webhook reconciliation has a 45-second
processing deadline. Raw provider payloads and credentials are not logged or persisted.

`POST /api/billing/sync` reconciles only the authenticated account, deriving its ID from the session.
`POST /api/billing/revenuecat/sync/{user_id}` is administrator-only and accepts `{import_stripe: false}`
for reconciliation or `{import_stripe: true}` to first submit the user's persisted Stripe Subscription
ID to RevenueCat's receipt-import API. It cannot import a caller-supplied subscription ID. An import
requires the RevenueCat Stripe-app public key. Provider-side imports cannot be undone by a local
database rollback; retrying the same receipt is safe. Both endpoints return the persisted status,
expiration, and scheduled-cancellation flag and are limited to `10/minute`.

These endpoints recover missed notifications and support explicit post-purchase reconciliation. There
is no periodic reconciliation job or RevenueCat SDK in the web frontend. Ordinary protected requests
use local state and do not depend on a live RevenueCat read. Revocation requires a successful webhook
reconciliation or explicit sync confirming an absent or expired entitlement, including any grace
period. If notifications are lost, the last confirmed state remains in effect until reconciliation;
operators must recover failed deliveries or use the sync endpoints. Existing Stripe state is preserved
until the first successful synchronization, so enabling the flag is not a substitute for importing and
reconciling existing subscribers.

## RevenueCat configuration and operation

1. Keep `REVENUECAT_ENABLED=false` while configuring the provider project. Connect the existing Stripe
   account to RevenueCat and attach the monthly/yearly Stripe products to the configured entitlement.
2. Add Stripe's RevenueCat webhook destination alongside FreeLingo's existing Stripe webhook. Enable
   tracking new purchases from server-to-server notifications and select the metadata detection method
   with field key `user_id`. Select only RevenueCat's documented Stripe events: `customer.subscription.created`,
   `customer.subscription.updated`, `customer.subscription.deleted`, `checkout.session.completed`,
   `charge.refunded`, and `invoice.updated`.
3. Import existing Stripe subscriptions using RevenueCat's receipt-import API with the same App User ID
   and each persisted `stripe_subscription_id`. Verify product-to-entitlement mappings and account IDs
   before switching access authority. Connecting Stripe alone does not backfill every subscription.
4. Configure the backend values from `.env.example`. Set up a RevenueCat webhook for all relevant apps
   in the project at `https://<public-host>/api/billing/revenuecat/webhook`, using the exact configured
   Authorization header and the matching environment. Coordinate delivery with enabling the backend
   flag; the route exists only when both billing flags are enabled.
5. Enable `REVENUECAT_ENABLED` and reconcile existing users through the administrator sync endpoint.
   The optional `import_stripe` mode supports explicit import repairs after activation. Check delivery
   results in RevenueCat and retry failed events or use reconciliation when its delivery retries are
   exhausted. Live purchase, renewal, cancellation, refund, and expiration checks belong to the deployment.

Disabling RevenueCat stops its synchronization and restores Stripe-only event handling. It does not
reconstruct Stripe access from a potentially cross-platform snapshot: reconcile existing accounts with
Stripe before relying on that rollback. `STRIPE_ENABLED=false` retains its independent bypass behavior.

Provider references:

- [Stripe renewal webhooks and backend access](https://www.revenuecat.com/docs/web/integrations/stripe#renewal-webhooks-and-access-on-your-backend).
- [External Stripe purchases](https://www.revenuecat.com/docs/web/integrations/stripe/track-external-purchases).
- [Stripe server notifications and metadata identity](https://www.revenuecat.com/docs/platform-resources/server-notifications/stripe-server-notifications).
- [Webhooks and customer reconciliation](https://www.revenuecat.com/docs/integrations/webhooks).

## Stripe card trial

Checkout includes `STRIPE_TRIAL_DAYS` only when the configured value is positive and `trial_used` is
false. Abandoning checkout does not consume the right. Verified Stripe snapshots with `trialing` status
or a non-null `trial_start` mark the trial as used, including when notification arrives after conversion
to a paid subscription. Administrative access overrides do not mark it.

The landing pricing subtitle, monthly badge, and all paid-plan CTAs advertise a Stripe trial only
when configured trial days are positive and the user has not already used it. Otherwise, the subtitle
uses the monthly/yearly plan-selection text, the monthly badge says Premium, and paid-plan CTAs use
the plan-selection label. When a trial is available, the subtitle displays its configured duration,
identifying it as additional trial days on subscription, with the card requirement and the paid
plan price applying afterwards. Without a subscription trial, the subtitle states that the paid
subscription starts on purchase. Paid cards also show the existing trial/payment terms next to
their CTAs. The landing defaults missing Stripe trial days to zero.

The Stripe card trial and the freemium no-card trial are independent. A Stripe `trialing` status has
subscription precedence and does not consume freemium counters.

## Freemium trial

When Stripe and `FREEMIUM_TRIAL_ENABLED` are active, eligible registration creates a no-card trial
ending after `FREEMIUM_TRIAL_DAYS` and marks it granted. Eligible older or admin-created users can
receive it best-effort when their profile is first loaded.
If that optional write fails, the profile endpoint rolls back the transaction and reloads the
persisted user before responding. A later profile read can retry the ungranted trial. Database
failures that also prevent reloading the user still fail the request.

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

Zero means unlimited for weekly sessions, daily/weekly minutes, and monthly tokens. Maximum duration
and inactivity are bounded settings instead: configuration and profile updates accept 900 or 1800
seconds for maximum duration, and 60, 180, or 300 seconds for inactivity. Zero is not an unlimited
option for these settings. Verified checkout activation resets quotas and timeouts from configured
defaults. Administrators may override them regardless of Stripe state.

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
It blocks chat, voice conversation, Listening, Reading, and game creation for non-admin users with
HTTP `503` or WebSocket close 1013. Administrators bypass maintenance. Saved game sessions and other
learning areas remain available.

Redis failure while checking maintenance is fail-open. Maintenance is checked when requests or
WebSocket sessions start; changing the flag does not terminate existing sessions. Frontend gates
replace the affected pages, but open clients do not receive push updates when the flag changes.

## Administration

Administrative APIs expose subscription fields and accept subscription filtering and recognized
status overrides. Moving a user from non-premium to `active` or `trialing` applies default quotas;
setting `none` clears the end date. Overrides update local access only and do not modify Stripe.
In RevenueCat mode they do not modify RevenueCat either and can be replaced by the next reconciliation;
durable provider-managed grants must be configured in RevenueCat. Quota overrides are retained across
ordinary renewals and duplicate notifications.

With Stripe disabled, frontend administration:

- hides active/trialing metrics and past-due alerts;
- hides and ignores subscription filters and values in the user list;
- hides subscription details and override controls;
- preserves quota controls.

Backend admin responses and update capabilities still include Stripe fields regardless of the
frontend toggle. The UI's monthly/yearly override maps locally to active access plus an approximate
30/365-day date; the actual billing interval is not persisted on the user.

## Frontend behavior

The config store loads public runtime flags. The freemium store caches status for 60 seconds within
the current authentication session. A synchronous auth subscription clears the snapshot, loaded flag,
and cache timestamp on logout or session replacement, before another account can reuse them. Token
rotation and language switches preserve the cache because quotas are global per user. Until the new
session loads its own status, including after a failed GET, the snapshot stays null: quota banners
show no balance and quota-based paywalls do not infer exhaustion. Backend access checks remain
authoritative, and a later fetch can retry.

The store provides optimistic decrement for chat, Listening, and Reading. A delayed chat completion
can decrement only its originating authentication session. Lessons refresh authoritative status after
completion; voice refreshes after session end. Quota GETs reject superseded requests and old-session
responses, including delayed body decoding; reads overlapping confirmed consumption reconcile again.

`FreemiumQuotaBanner` shows active-trial time, remaining/limit values, Premium-only state for zero
limits, and low-balance emphasis. `PaywallBanner` renders inline upgrade or payment-recovery actions.
There is no `PaywallGate`; each feature page adapts only the consuming controls while preserving
readable history where backend policy permits.

Paywall and Settings plan actions share `lib/billing.ts`. On `409 subscription_already_active`, they
reload `/api/auth/me` and update the authenticated profile; only a refreshed `active` or `trialing`
status resolves the conflict successfully. Other conflicts, failed reads, or a non-Premium profile
retain the checkout error and permit retry. Unmounted or replaced-session requests cannot publish
profiles or redirect the browser. This recovery reads the locally persisted profile rather than
starting another provider synchronization.

`past_due`, `unpaid`, and `paused` use Customer Portal recovery. `none`, `incomplete`,
`incomplete_expired`, and `canceled` offer monthly/yearly checkout.

Landing pricing exists only when Stripe is enabled and the visitor is not known to be subscribed.
Its heading is deployment-neutral and its context identifies prices as belonging to the current
installation. Self-hosting does not require an official FreeLingo Cloud subscription; the operator
configures access and limits. Stripe being enabled must not label an arbitrary installation as Cloud.
The free card and anonymous signup notes describe initial no-card Premium access when the public
`freemium_trial_enabled` flag is true, followed by limited free access unless the learner subscribes.
With the flag off, they describe limited free access directly. No fixed signup-trial duration is
promised because public config does not expose `FREEMIUM_TRIAL_DAYS`. The comparison separates
the ungated study plan from limited lesson completion and lists games among limited features.
The card-based subscription trial uses the configured duration and eligibility above. Public FAQ
copy distinguishes initial no-card Premium access from the optional additional subscription trial.
It explains that
subscribing starts the paid subscription unless additional trial days are explicitly offered, and
does not present self-hosting as free infrastructure or necessarily local processing.
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
