---
description: "Situations catalog, localized discovery, plan-owned role-play context, and entry into existing voice conversation."
applyTo: "backend/app/{data,routers,schemas,services}/situations.py, backend/app/services/prompts/tutor.py, frontend/src/app/(app)/situations/**, frontend/src/lib/situations.ts, messages/*.json"
---

# Situations

## Purpose and ownership

Situations offers everyday role-play with Lingu through the existing voice conversation flow.
The authenticated `/situations` catalog appears as Everyday situations (localized through
`nav.situations`) under Practice in the shared desktop/mobile navigation.
It requires an owned active study plan; the plan supplies the target language and CEFR level.

This specification owns the catalog, discovery interface, scenario context, and learning flow.
`voice-conversation.instructions.md` owns microphone startup, speech, transport, persistence, and
session lifecycle. `subscriptions-freemium.instructions.md` owns access and quota accounting;
`api-endpoints.instructions.md` owns wire-level fields and errors.

## Canonical catalog

`backend/app/data/situations.py` owns the stable situation IDs, category membership, roles, scenario,
and learner objective. The catalog contains five categories with ten situations each, combining
straightforward everyday exchanges with scenarios for resolving practical problems:

- `daily_life`: `medical_appointment`, `neighbour_problem`, `flat_viewing`, `school_meeting`,
  `household_repair`, `recount_day`, `weather_chat`, `daily_routine`, `household_chores`,
  `plan_dinner`.
- `travel`: `change_reservation`, `hotel_problem`, `ask_directions`, `missed_connection`,
  `lost_luggage`, `buy_ticket`, `hotel_check_in`, `taxi_ride`, `collect_key`, `local_recommendations`.
- `shopping_services`: `return_purchase`, `restaurant_order`, `phone_contract`, `bank_appointment`,
  `delivery_problem`, `bakery_purchase`, `clothes_shopping`, `cafe_order`, `haircut_appointment`,
  `supermarket_help`.
- `social`: `meet_someone`, `make_plans`, `decline_invitation`, `resolve_misunderstanding`,
  `host_visitors`, `congratulate_friend`, `hobbies_chat`, `family_chat`, `invite_friend`, `choose_gift`.
- `work`: `introduce_yourself`, `explain_task`, `clarify_instructions`, `negotiate_deadline`,
  `share_proposal`, `late_arrival`, `work_update`, `arrange_meeting`, `colleague_help`, `break_chat`.

The authenticated catalog response supplies IDs/category membership and the resolved plan, language,
and level. It does not accept caller-authored role-play instructions. Interface category labels,
titles, descriptions, and controls live in the `situations` namespace in all UI translation catalogs.
Those labels follow the interface locale, independently of the language being practised.

## Discovery and presentation

The page follows the established practice-page layout, solid `fl-*` surfaces, petroleum-blue accent,
and monochrome controls. Category filters and search share the catalog's presentation; search matches
the translated title, description, and category label. Category labels and situation cards sort alphabetically using
the active interface locale's collation. The Practice navigation link uses the shell's same translated
sorting policy.

Loading, recoverable errors, and an empty search result are distinct from a missing plan.
A confirmed missing plan shows the shared `NoPlanBanner` and its assessment action. Selecting another
study language must load that language's plan context before presenting a usable start action.
Pending or obsolete catalog responses must not supply context to a different account or language.

Selecting a situation enters the existing voice conversation interface with its stable ID and the
catalog's captured study-plan ID. The catalog and voice-entry title are interface-localized;
the saved conversation title instead retains the canonical English scenario title with a
native-language practice prefix, as specified in `voice-conversation.instructions.md`.
Learned-language transcript
content continues to use `TargetLanguageText`. Contextual entry replaces unrelated conversation
starters while retaining the existing microphone, playback, stopping, and recovery controls.
If a quota blocks entry, restoring access enables a manual start rather than automatically opening
the microphone. Exhausting the Situations allowance does not replace the displayed remaining voice
minutes with zero or interrupt an already admitted session.

## Source resolution

The voice authentication payload carries `situation_id` and `situation_study_plan_id` together.
This source is mutually exclusive with lesson practice, Grammar Practice, and the post-assessment
voice demo, including conflicting fields explicitly sent as null. An active no-card freemium trial
remains an ordinary access entitlement.

The backend resolves the canonical situation and verifies the supplied active plan belongs to the
authenticated learner before quota consumption. Plan and language-track ownership must agree, and
their persisted target languages must match a supported canonical code. The plan must be active in
its owning track; the track need not be the currently selected language. The persisted plan determines language, CEFR level,
and provenance; client target language, free-form context, and conversation identity cannot replace
that source. A missing, inaccessible, or inactive plan must not fall back to another plan or language.
Each start is a separate voice conversation.

`services/situations.py` composes an escaped JSON reference containing the canonical situation data,
target language, and CEFR level and passes it through the existing `lesson_practice_context` input.
The server-generated `<situation>` prefix selects the role-play branch in the prompt builder;
lesson and Grammar Practice references retain their existing wrapper.
The context remains available for the greeting, normal turns, memory refreshes, and tool-free
fallbacks without a second speech pipeline or a separate text-practice mode.
The source context is session-local; ordinary voice transcript history remains the saved record.

Selected transcript words carry the same situation/plan pair to `/api/flashcards/from-word`.
The backend resolves lookup language, CEFR level, deduplication, and destination from that owned
plan, including after it becomes historical or the active selection changes. Unknown situations
and unavailable plans fail without active-plan fallback. This save validates the catalog and plan
ownership; it does not require a persisted role-play completion record or consume a Situations start.
Input validation and response errors belong to `api-endpoints.instructions.md`.

## Role-play guidance

The context identifies the setting, Lingu's role, the learner's role, and a concrete communicative
objective. Instructions adapt vocabulary, complexity, and support to the plan's CEFR level and
resolved target language:

- Open directly in character in one or two short sentences and let the learner produce meaningful language.
- Respond to the learner's actual contribution rather than following three predetermined questions.
- Keep turns concise, ask at most one useful question at a time, and offer brief hints or reformulations
  when needed. Use fictional details rather than requesting real credentials or sensitive records.
- Work toward the objective through the learner's own explanation, clarification, choices, and
  agreement as appropriate to their level. Solving everything for them is not sufficient practice;
  perfect grammar is not a prerequisite for resolving the practical objective.
- Introduce relevant variations when useful without padding or manufacturing obstacles after resolution.
- Once sufficiently practised and resolved, confirm the agreement or next step, then briefly speak as
  Lingu with specific feedback from the available conversation and one useful improvement if warranted.
  Do not invent success, pronunciation assessments, or evidence from forgotten turns.
- If the learner continues, help naturally without repeatedly announcing completion.

These are conversational instructions, not deterministic grading or a fixed turn count.
A verbal conclusion does not emit `session_end` or close the WebSocket; the learner can continue or
stop within the existing voice limits. Shared tutor and native-language-help policies still apply.

## Access and usage

Loading or filtering the catalog and voice warmup do not consume an attempt. Starting a situation requires its
feature allowance as well as ordinary voice access and general conversation limits.
The Situations allowance is global across study languages and is recorded once per normal session
admission, not per turn or completed objective. Admission does not guarantee a successful greeting or
first audio. Its configured default, reset, exemptions, and status fields are defined in
`subscriptions-freemium.instructions.md`.

Voice duration, session/minute/token limits, maintenance, transcript persistence, and rewards follow
the existing voice contract. Resolving a role-play objective creates no separate completion record,
score, or additional reward.
