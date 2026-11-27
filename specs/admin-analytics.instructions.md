---
description: "Internal admin reports of retained learning activity, feature adoption, activation, and retention."
applyTo: "backend/app/{routers,services,schemas}/admin_analytics.py, frontend/src/app/(app)/admin/**, frontend/src/components/admin/**"
---

# Admin analytics

## Population and time

Reports cover accounts whose current role is `user`, including disabled learner accounts with
historical activity. The enabled-account count in the operational overview is a separate account
state. Reports describe study activity, not visits, sign-ins, time spent, or people online.

All windows use complete UTC calendar days and exclude today. A practice day is any retained
`progress` row, including zero-XP activity. Count the learner once per day across plans and
languages; count unique learners over a window rather than summing daily counts.
Deleted accounts, plans, and resources can change historical totals. Reports describe retained
evidence and do not maintain a separate event history.

## Activity and cohorts

- The overview shows one chart: learners who practised on each of the last 30 complete days.
  An observed day without activity has value zero. A failed request is not an empty period.
- The detail page shows distinct learners over 7 and 30 days and learners active on at least two
  different days in the last 7. Each is compared with the immediately preceding window of equal length.
- The account distribution includes all learner accounts created before today's UTC cutoff.
  Classify each by its latest retained practice before the cutoff: 1–7 days ago, 8–30 days ago,
  more than 30 days ago, or no practice recorded. Shares use this entire population.
- For each of the last eight complete Monday–Sunday weeks, partition practising learners into
  first-time (first retained practice that week), continuing (also active the previous week),
  or reactivated (earlier practice, absent the previous week). Show previous-week learners
  absent that week separately; they are not part of its active total. The first displayed
  week also uses its actual preceding week. A missed week does not imply permanent churn.
- The frequency histogram counts learners with 1, 2–3, 4–7, 8–13, or 14–28 distinct days
  of practice in the last 28 complete days. It excludes learners without practice in that window.
- Activation groups accounts by registration week (Monday to Sunday UTC). Show the eight most
  recent weeks for which the entire cohort has had the registration day and six subsequent days.
  Count registrations, learners who created a retained plan, and those who subsequently recorded
  practice in that window. Inactive plans remain eligible; each account contributes once per step.
- Retention groups learners by the week of their **first retained practice day**. Show the last
  eight complete weeks and count a return on any day from day 7 through day 13 inclusive,
  relative to each learner's own first day. Until the last day of a cohort has had the full
  observation window, its return count is unavailable. Empty groups display “No learners” instead
  of a percentage; zero returns among an observed, nonempty cohort is 0%.

## Usage by feature

The 7-, 30-, and 90-day selector applies only to usage by feature. Bars compare distinct
learners; volume is expressed in a feature-specific unit. A learner can appear in multiple bars.
The list sorts by translated feature name using the active interface locale.
The repeat-usage column counts learners with confirmed use of that feature on at least two
distinct UTC dates in the selected window, as a share of its own learners. The definitions
below apply to both counts; completing two actions on the same day does not qualify as repeat usage.

- Lessons: learners who submitted an exercise (`answered_at`) or completed a lesson
  (`completed_at`); volume counts completed lessons.
- Reading and Listening: submitted attempts by `completed_at`, including replays and zero scores.
- Games: completed sessions by `completed_at`. A partial game can contribute to daily progress
  without appearing as a completed game here.
- Grammar Practice: accepted answers by their individual `answered_at`, including answers in
  sessions that were later abandoned.
- Lingu chat and voice: answered turns by the timestamp and recorded modality of the reply.
  Count an explicitly linked nonblank learner/assistant pair from the same account, conversation,
  and modality. Greetings, unanswered messages, and legacy turns without pairing or modality are
  excluded. Voice volume counts answered turns, not microphone time.
- Flashcard reviews contribute to daily practice. Their receipts have no review timestamp and are
  not used to build a feature series.

## Query lifecycle

The overview requests only its operational stats and the daily series. The detail response includes
that same cached series with the same UTC cutoff as the rest of the report, including when a range
change crosses midnight. No shared navigation, learner request, polling loop, or
scheduled job computes these reports. The backend requires an authenticated administrator before
reading any cached data; responses contain only aggregate dates and counts, never identities,
answers, or conversation text.

Redis caches the series, fixed-window aggregates, and range-specific feature totals separately
for five minutes, keyed by the exclusive UTC cutoff and, for feature usage, the selected range.
On a cache miss the detail endpoint uses a repeatable-read PostgreSQL snapshot, so concurrent
data deletion cannot split the fixed-window calculations across different database states.
After the standard rate-limit check, a failed report-cache read falls back to the database.
The limiter itself retains its existing Redis dependency. HTTP clients must not cache
these private responses. See [API endpoints](api-endpoints.instructions.md) for the wire contract.
