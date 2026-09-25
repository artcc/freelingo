---
description: "Current-state specification for Grammar, Vocabulary, Phrasebook, progress and competencies, placement-bank resources, and level-completion tests."
applyTo: "backend/app/data/**, backend/app/models/{resource_native_help,progress,competency}.py, backend/app/routers/{grammar,vocabulary,phrasebook,progress,assessment,curriculum}.py, backend/app/services/{resource_native_help,progress_service,assessment}.py, frontend/src/app/(app)/{grammar,vocabulary,phrasebook,progress,assessment,plan}/**, frontend/src/data/curriculum.ts"
---

# Learning Resources

## Purpose and source of truth

Grammar, Vocabulary, Phrasebook, curriculum, and assessment-bank content is defined in backend Python
dataclasses grouped by target language and CEFR level. The frontend retrieves these resources through
authenticated APIs; it does not contain the canonical datasets.

All ten supported target languages provide A1-C2 curriculum, grammar, vocabulary, phrasebook, and
placement-bank data. Dispatchers select exact English variants and ISO-prefix packages for other
languages. Unknown dispatcher input currently falls back to `en-GB` rather than returning an error.

Static resource APIs accept an explicit language query and do not require it to match the user's
active language or owned plans. Frontend resource pages normally send the active language, with
`en-GB` fallback.

## Shared native-language help

Grammar, Vocabulary, and Phrasebook can generate additional help in the authenticated user's native
language. The client chooses target resource/language but cannot override native language.
Help labels resolve the profile's native-language code through the UI locale's `languages` catalog;
`targetLanguages` names only learning languages and cannot label every native language.

Generated help is cached globally in `resource_native_helps` by resource type/key, target language,
native language, and source-content hash. Changing hashed source data invalidates the cache.

Redis uses a 90-second generation lock. A request that finds another generator waits through short
database checks and returns cached content if it appears; otherwise it returns `503` asking the caller
to retry. LLM failures also return `503`.

The lock-acquisition path does not treat every false-like Redis result identically, so strict
single-generation behavior is not guaranteed under all Redis return/failure conditions.

## Grammar reference

Each `GrammarTopic` contains slug, title, CEFR level, free-form category, summary, explanation,
optional structure, rules, examples, common mistakes, and related slugs. Examples use target `text`
with optional translation and note.

Categories are language-specific strings, not a universal 14-value backend enum. Slugs and related
references are checked by data-integrity tests. Lesson grammar references are restricted to slugs
declared by the selected language curriculum, not one fixed global list.

- `GET /api/grammar`: authenticated, `60/minute`; returns all complete topics for the language.
- `GET /api/grammar/{slug}`: authenticated, `60/minute`; returns one topic or `404`.
- `POST /api/grammar/{slug}/native-help`: authenticated, `10/minute`; returns cached/generated help,
  `404` for unknown slug, or `503` when unavailable.

The index groups by CEFR level and searches title, summary, and category. Categories are derived from
returned data. Detail currently loads the full collection and locates the slug locally rather than
calling the single-topic endpoint.

Detail renders explanation, structure, rules, examples, mistakes, and related links. Example
translations returned by the API are not displayed. A1/A2 native help opens and generates on load;
B1-C2 generates when opened. Grammar pages do not provide TTS, flashcard creation, or automatic
current-slug chat context. Lesson `grammar_refs` provide the implemented cross-link.

## Vocabulary hub

A `VocabularySet` contains ID, CEFR level, topic, curriculum `unit_ref`, and entries. Each entry
contains target-language word, part of speech, target-language definition and example, plus optional
IPA and frequency rank. Set IDs need only be unique within one target language; size varies by
language.

- `GET /api/vocabulary`: authenticated, `60/minute`; returns complete sets and entries.
- `GET /api/vocabulary/level/{level}`: authenticated, `60/minute`; level is case-insensitive and an
  invalid level returns `400`.
- `GET /api/vocabulary/{set_id}`: authenticated, `60/minute`; returns one set or `404`.
- `POST /api/vocabulary/{set_id}/native-help`: authenticated, `10/minute`; uses the shared cache and
  returns `404`/`503` under the shared rules.

The index groups and filters by level and searches set topic or ID; it does not search inside words
or show deck coverage. Detail shows word, part of speech, IPA, frequency, definition, and example.

The available deck action adds the entire set through flashcard bulk creation. There is no per-entry
add control. Bulk creation requires the active plan and deduplicates normalized words within it. The
page currently sends an empty translation and the bulk endpoint does not generate one.

Vocabulary native help begins collapsed and is generated on request. Progress treats an item as
covered only when its plan-owned flashcard has `repetitions > 0`.

## Phrasebook

Each category contains ID, CEFR level, situation, icon, and phrases. Phrases contain target-language
text, context, register (`formal`, `neutral`, or `informal`), optional unit reference, and optional
romanization. CJK resources provide romanization data, though the current page does not display it.

- `GET /api/phrasebook`: authenticated, `60/minute`; returns all categories.
- `GET /api/phrasebook/level/{level}`: authenticated, `60/minute`; invalid level returns `400`.
- `GET /api/phrasebook/{category_id}`: authenticated, `60/minute`; unknown category returns `404`.
- `POST /api/phrasebook/{category_id}/native-help`: authenticated, `10/minute`; uses shared cache.
- `GET /api/phrasebook/audio/{category_id}/{phrase_index}`: authenticated, `30/minute`; returns
  cached MP3, `404` for invalid category/index, or `503` without TTS.

Phrase audio is stored below `{AUDIO_STORAGE_PATH}/phrasebook/{iso}/` under a hash of language,
category, index, and text. Generation writes a temporary file and replaces atomically. Responses use
a one-day public cache header. The endpoint sends text to TTS without an explicit language argument.

The page filters A1-C2, register, and target text. It searches phrase text but not context. Categories
display phrases directly rather than through expansion controls. Each phrase has explicit audio and
copy buttons; clicking text itself does not copy.

A1/A2 help panels begin open but generation still requires button action. B1-C2 begins closed. Help
state can survive an active-language change when category IDs are reused. Phrasebook does not create
flashcards.

## Progress and competencies

Progress has daily rows per user, plan, and date with XP, lessons, exercises, streak, and skill JSON.
`UserCompetency` stores one row per user, plan, unit, and competency text.

Exercise skill uses lesson type as its key. Updates apply `0.7 * previous + 0.3 * latest`; a new skill
starts at the latest score. Lesson completion applies the lesson's mean answered-exercise score, or
0.5 when none is available, to every competency in the unit. Mastery is `score >= 0.80`.

- `GET /api/progress/summary`: authenticated, `60/minute`; summarizes the active plan, returns zeros
  without one, and exposes skill JSON from the latest daily row.
- `GET /api/progress/history`: authenticated, `60/minute`; returns up to 90 recent daily rows.
- `GET /api/progress/competencies`: authenticated, `60/minute`; returns unit ID, average score,
  mastered count, and total count, or an empty list without a plan.

The Progress page does not request daily history. It combines summary, unit aggregates, plan,
curriculum, and flashcards. Because the API does not return individual competency status, the page
presents the first `mastered_count` curriculum competencies as mastered and cannot identify the
actual mastered items. Unit bars use mastered count rather than average score.

Vocabulary coverage is calculated from reviewed plan-owned cards. Skill display uses the latest
daily skill JSON and may contain any lesson-type key, not only four fixed skills.

## Placement assessment bank

The placement bank contains target-language questions across A1-C2 and grammar, vocabulary, and
reading. Questions include ID, skill, difficulty, prompt, options, correct option, and optional
grammar slug.

- `GET /api/assessment/bank`: authenticated, `60/minute`; returns the bank including correct answers.
- `POST /api/assessment/evaluate`: authenticated, `60/minute`; evaluates submitted answer records.
- `POST /api/assessment/complete`: authenticated, `10/minute`; creates the selected-language plan.

The client calculates each `correct` boolean. Evaluation trusts submitted question metadata and does
not retrieve the bank to verify selected options. The deterministic algorithm is described in
`platform.instructions.md`.

Legacy `/assessment/start`, `/submit`, and `/free-write` LLM endpoints remain available but are not
used by the current assessment page.

## Level-completion test

The level test unlocks when the learner reaches the plan's final position
(`progress_day >= duration_weeks × days_per_week − 1`) and no lesson from a passed day is still pending.
Skipped lessons keep the assessment locked until completed and remain reachable through
`/pending-lessons`. Unit competency is informational and does not gate the assessment; the test's own
recommendation handles reinforcement. A persisted result keeps the flow eligible so existing
submissions are never refused. Eligibility is enforced by the backend, not only by a frontend button.

- `GET /api/assessment/level-test/questions/{plan_id}`: authenticated, `5/minute`; gathers grammar
  and vocabulary identifiers from the plan language/level curriculum and asks the LLM for a test.
  Returns 403 before the final position or while a passed-day lesson is pending, unless a result is
  already persisted.
- `POST /api/assessment/level-test/submit`: authenticated, `10/minute`; evaluates submitted answer
  records and persists score/recommendation on the plan. Applies the same eligibility rule and returns
  403 before the final position or while a passed-day lesson is pending, unless a result is already
  persisted.
- `GET /api/assessment/level-test/result/{plan_id}`: authenticated, `60/minute`; returns a recorded
  result. It requires a persisted result and is not affected by eligibility.

The prompt requests 20 questions across grammar, vocabulary, and reading, but generated JSON is not
validated by a Pydantic question schema and correct options are returned to the browser. Submit does
not bind answers to a stored session, verify them against generated questions, require 20 answers, or
prevent resubmission; its only eligibility gate is the final-position and pending-lessons rule above.

Recommendation thresholds are `advance` at 0.75 or above, `extend` from 0.55 to below 0.75, and
`repeat` below 0.55. Score is the mean of three skill profiles, including zero for an absent skill.

Recommendations are persisted, but current frontend actions only navigate to Assessment or Plan.
They do not automatically create a next-level plan, extend duration, focus weak units, or archive and
repeat a plan.

## Navigation

Grammar, Vocabulary, and Phrasebook appear in the Resources group on desktop and mobile. Progress
and Assessment remain learning pages. Middleware checks refresh-cookie presence and every resource
endpoint independently requires backend authentication.

## Related specifications

- `platform.instructions.md` — onboarding and placement journey.
- `study-plan.instructions.md` — curriculum distribution and lesson lifecycle.
- `target-language.instructions.md` and `add-target-language.instructions.md` — language data rules.
- `speech-services.instructions.md` — phrase audio.
- `database-models.instructions.md` and `api-endpoints.instructions.md` — complete contracts.
