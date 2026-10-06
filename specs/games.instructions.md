---
description: "Games catalog, Error Detective, Sentence Order and Vocabulary Pairs: personalized generation, plan-owned sessions, quotas, rewards and audio."
applyTo: "backend/app/{models/game,schemas/games,routers/games,services/games,services/prompts/games}.py, frontend/src/app/(app)/games/**, frontend/src/components/games/**, frontend/src/lib/{games,detective,sentence-order,vocabulary-pairs}.ts, messages/*.json"
---

# Games

## Route and access

`/games` belongs to the authenticated app layout and the middleware's protected-route list.
The shared main navigation places Games after Conversation in desktop and mobile menus.
The catalog page has no subscription restriction or Premium badge.

## Catalog and empty state

`frontend/src/lib/games.ts` exports `availableGames`, a readonly list of navigation metadata:
stable ID, `/games/` route, and title/description keys in the `games` translation namespace.
Only implemented games with working routes and translations belong in this list.

The catalog links to Error Detective at `/games/error-detective`, Sentence Order at
`/games/sentence-order` and Vocabulary Pairs at `/games/vocabulary-pairs`.
All use the shared catalog component. If no definitions are registered,
the existing localized empty state links to `/plan`. Navigation metadata is presentation only.

## Error Detective

A game contains five short sentences, each with one error repaired by replacing one existing
fragment. There is no timer. Each challenge has two persisted steps, with one choice per step:

1. Select a fragment. The backend then reveals the incorrect fragment and three correction options.
2. Select a correction. The backend then reveals the correct option, corrected sentence and explanation.

An incorrect detection still permits correction practice. Both steps must be correct for the
challenge's XP bonus. Answers are deterministic comparisons against persisted content, not new LLM
evaluations. Challenges must be answered in order. Repeating the same answer is idempotent; trying
to change it returns 409. Future solutions and correction options are excluded from public responses.

## Sentence Order

A game has five short sentence-building challenges, without timers or lives. Each supplies a brief
native-language clue and 3–12 target-language fragments. Learners tap fragments into a sentence;
tapping a placed fragment returns it to the pool. Buttons support keyboard and touch input without
requiring dragging. A preview joins fragments with the persisted separator, preserving exact text.
Only a complete permutation can be submitted, once per challenge, in challenge order.
Draft arrangements are local; submitted answers survive navigation and reloads.

Each private challenge contains one canonical sentence, clue, fragments, separator (`""` or `" "`),
one to eight distinct accepted orders, explanation and source ID. Every order uses each index exactly
once and the first reconstructs the canonical sentence exactly. Fragments have no boundary whitespace;
punctuation remains attached to meaningful text. CJK uses natural chunks and writing, without invented
spaces or romanization. The generator avoids sentences with more alternatives than the bound allows.

An independent semantic review checks validity and completeness of accepted arrangements against the
clue, as well as source scope, level, regional language, segmentation and native explanations. This
reduces ambiguity but cannot prove linguistic completeness. Before persistence the server shuffles
fragments and remaps all accepted orders, requiring an initially unsolved arrangement. Five valid,
reviewed challenges are required before consuming quota.

Evaluation compares reconstructed text with the saved accepted sentences, so identical repeated
fragments are interchangeable. No per-answer LLM call is made. Malformed permutations and answer
shapes from the other game return 422. Exact retries return saved state; changing a submitted order
returns 409. After answering, the API reveals correctness, explanation and the full correct sentence:
the submitted variant if accepted, otherwise the canonical solution. Solutions and accepted orders
are never exposed before submission. Results show submitted mistakes for review; only correct text
is sent to the shared audio player.

## Vocabulary Pairs

A game has five target-language terms or short expressions and five native-language meanings in
independently shuffled columns. No timer or lives apply. Learners select one item from each column
with keyboard-operable buttons, may change their selection, then explicitly check the pair.
Pairs can be solved in any order. A correct pair is disabled in both columns and its term can be
played through `AudioPlayer`. An incorrect combination leaves both items available for other matches.
Previously tried combinations cannot be submitted again as new attempts.

Each private pair stores its term, meaning, target-language example sentence, native translation,
source ID and randomized meaning index. Structural validation requires exactly five distinct,
nonempty terms and meanings after Unicode normalization and case folding. The independent semantic
review checks all 25 possible correspondences and rejects ambiguous/overlapping meanings, unsupported
terms, incorrect languages or examples. This is not a formal linguistic guarantee. CJK preserves
natural script and spacing; source glosses are translated to the captured native language.

Attempts persist with a zero-based sequential number, term index, meaning index and correctness.
Exact retries return current saved state; conflicting reuse of an attempt number, stale/future
attempts, already-solved items or previously tried combinations return 409. At most 25 distinct
combinations exist. Reloading recovers failures and successes without resubmitting uncertain work.
Wrong attempts mark BOTH involved pairs as assisted, permanently losing their first-try bonuses.
This flag is private until that pair is solved, so it cannot reveal the other term's correct meaning.

Completion awards 5 XP plus 2 per pair never involved in an incorrect attempt. Only when all five
pairs are solved are their example sentences and translations revealed for review. Abandonment
retains solved pairs and attempt history without XP, new examples or a quota refund.

## Context and modes

New creation requests require an active owned study plan and an expected plan ID; a missing active
plan returns 404 and a mismatch returns 409. Retries of accepted request UUIDs resolve their persisted
result and validate the original parameters without requiring an active plan, even when the active
language has no plan.
Existing session operations authorize their persisted owner and plan independently of active selection.
Target language and CEFR level come from that plan. Native language is captured from the profile for
generated explanations; interface controls use the current UI locale. Changing preferences does not
rewrite existing content. Target-language text uses `TargetLanguageText` and exact regional overlays.

- `review`: up to twelve recently completed lessons of the owning plan, with bounded content and
  recent incorrect exercise answers. Incomplete lessons are not sources.
- `prepare`: the next incomplete teaching slot at or after `progress_day` in the persisted schedule.
  Completed lessons from its unit or its curriculum prerequisite unit supply the known material.
  Upcoming objectives guide relevance but do not authorize testing new material. Final assessment
  slots are excluded. Missing upcoming slots or completed sources disable the mode with guidance.
- `free`: a sample of up to eight canonical grammar topics at the plan language and CEFR level.
  Vocabulary Pairs instead samples up to four canonical vocabulary sets at that language/level,
  with up to twenty entries per set. Completed lessons are not required; a missing plan leads to
  assessment guidance.

Recent game sentences discourage repetition and incorrect answers inform practice priorities.
Context lookup does not call `/study-plan/today`, generate lessons, or advance the plan.

## Generation and recovery

`POST /api/games/{game_type}`, accepting `detective`, `sentence-order` or `vocabulary-pairs`, persists a UUID-keyed
session and returns 202. FastAPI background work
uses an independent database session and the shared structured-output adapter. No provider call
holds an open database transaction. The inference deadline comes from
`EXERCISE_GENERATION_TIMEOUT_SECONDS`; the adapter receives the remaining monotonic budget.

For Detective, Pydantic requires five distinct sentences, three distinct options, valid indices and exact fragment
reconstruction/replacement. Fragments retain spaces and punctuation and support CJK without inserting
word separators. Every challenge cites an allowed source. A separate structured LLM review checks
linguistic validity, unique correction, language, level and source scope. At most two candidates are
generated within the same budget. Semantic review reduces ambiguity but is not a formal proof.

Sessions have `generating`, `ready`, `completed`, `failed`, or `abandoned` state. A partial unique
index permits one generating/ready session per plan and game type. Repeated starts return the existing active
session of that type. Every accepted creation UUID is persisted in `game_requests` with its submitted plan/mode/type
and the returned session ID, including when an active game is reused. A retry returns that same
session even after completion or abandonment or a change of active language, without another
reservation. A repeated request UUID
cannot change its submitted mode, plan or game type. Deleting the session leaves the request identity reserved;
recovery then returns 404 and creation retries return 409. Expired generations become failed on
lookup/start; late workers cannot publish content after the persisted deadline or replace terminal
state. This is not a durable job queue: process interruption is recovered as a deadline failure.

The browser uses bounded requests and non-overlapping status polling. An uncertain start is recovered
by GET using its request UUID; an uncertain answer is recovered by reloading the session, not by
resubmitting it. Ready games are resumable through their URL and game-type/language-filtered paginated history.
Session endpoints accept both canonical IDs and owned creation UUIDs, and return the canonical ID.
Leaving the catalog cancels its current request; late creation success/failure cannot navigate away
from the user's next page.
Leaving preserves progress. Explicit abandonment closes a ready game without XP or quota refund.

## Admission, activity and XP

`FREEMIUM_GAMES_DAILY` defaults to three new games per user/UTC day across languages and game types. Zero blocks
new free games. Active/trialing subscriptions, active freemium trials and Stripe-disabled deployments
bypass this quota. Normal maintenance blocks new generation for non-admins; saved games remain usable.

Admission uses PostgreSQL, not the best-effort Redis counters of other features. Under a user-row
`FOR NO KEY UPDATE` lock, a new session reserves a slot. Valid content and consumption commit together;
generation failure releases the reservation. Expired reservations no longer count. The reservation's
creation UTC date owns its consumption even if generation finishes after midnight. Admission records
survive plan/language deletion and cascade only with the account. Finishing/resuming requires no new
admission, even after subscription expiry or quota exhaustion.

Each newly accepted answer records activity in its plan on its captured UTC date. Completion awards
5 XP plus 2 per fully correct challenge (both Detective steps, the accepted Sentence Order submission,
or a Vocabulary Pair resolved without either item participating in an incorrect attempt),
capped at 45 game XP shared by all game types per plan/UTC day; remaining daily XP
can partially credit a game. All XP is awarded at completion. Session completion, reward ledger and
daily progress share one transaction, serialized by the owning plan and session. Duplicate requests
cannot repeat rewards. Games do not alter lesson completion, exercise counters, skill EMA or competencies.

## Audio

After answering, the full correct sentence uses the existing `AudioPlayer`, TTS proxy and backend
provider/voice rules, exactly as lesson examples. Explanations and erroneous sentences are not sent
to speech synthesis. Playback is optional and does not gate completion or XP.
Vocabulary Pairs plays only the resolved target-language term or expression, never the native meaning.

## Presentation and languages

The page uses the resource pages' `max-w-4xl` container, bordered header and surface panels,
responsive card grid, `fl-*` tokens, and existing light/dark themes. Interface text uses Geist Sans.
The title is an `h1`; the empty state and game cards use `h2` headings. Game pages reuse the shared
quota/paywall banners, confirmation dialog and pagination; choices are keyboard-operable buttons.

Navigation and game UI text are localized in all fifteen interface catalogs. The shared app shell
retains its language selector; a saved game continues to identify and use its persisted language.
