---
description: "Current-state specification for target-language codes, defaults, metadata, validation, initial selection, compatibility fields, regional prompt behavior, and speech-language conversion."
applyTo: "backend/app/schemas/auth.py, backend/app/models/{user,study_plan,user_language}.py, backend/app/services/language_helpers.py, backend/app/services/prompts/common.py, backend/app/data/**, backend/app/routers/{auth,languages,stt}.py, frontend/src/lib/target-languages.ts, frontend/src/components/TargetLanguageSelector.tsx, frontend/src/app/(auth)/{register,onboarding}/**"
---

# Target Language

## Purpose and scope

Target-language values use BCP-47 strings to identify the language and regional variety being
learned. This specification defines recognized codes, defaults, metadata, validation, initial
selection, and service conversion.

Active-language lifecycle, plan isolation, and language deletion belong to
`multi-language.instructions.md`. Adding another implemented language follows
`add-target-language.instructions.md`.

## Supported codes

The application recognizes `en-GB`, `en-US`, `de-DE`, `es-ES`, `fr-FR`, `it-IT`, `pt-PT`, `ja-JP`,
`ko-KR`, and `zh-CN`.

Backend `SUPPORTED_TARGET_LANGUAGES` and the frontend catalog must represent the same canonical set.
Validated account flows compare exact canonical strings; there is no general backend BCP-47 parser or
canonicalizer.

`AVAILABLE_TARGET_LANGUAGES` is the operator-enabled subset. Language-management and onboarding
surfaces expose the intersection of configured available codes and supported implementation.
Registration schema validation uses the supported set, while authenticated add/switch operations use
the available set.

## Default and fallback

`en-GB` is the application default and general runtime fallback for registration schema, ORM values,
study plans, chat/conversation fallback, frontend metadata, and static-resource dispatchers.
`en-US` is supported but must not be introduced as a new application fallback.

Static curriculum, Grammar, Vocabulary, Phrasebook, and assessment dispatchers currently fall back to
`en-GB` for unknown inputs rather than rejecting them. Validated product flows should still reject
unsupported codes before dispatch.

Earlier database migrations installed `en-US` server defaults on some columns. Ordinary application
creation paths provide `en-GB` explicitly through schema/ORM defaults; direct inserts relying only on
historical database defaults are not the supported application path.

## Metadata

Backend language helpers define English display and self names, ISO 639-1 conversion, flag, script,
romanization, word-spacing behavior, and comprehension length guidance.

Unknown backend codes retain their code as the display name, derive ISO from the prefix, use no flag,
and receive Latin-like capability fallbacks.

The frontend catalog defines canonical code, self and English names, flag asset, ISO code, script,
font class, word-spacing behavior, and optional romanization. Lookup is case-insensitive and returns
canonical metadata. Unknown frontend capability lookup uses Latin defaults.

User-facing language names are localized where message catalogs provide them. `TargetLanguageText`
uses script and font metadata for learned-language content independently from UI locale.

## Registration and initial selection

`POST /api/auth/register` accepts optional `target_language`, defaults it to `en-GB`, validates it
against supported codes, and stores it in `users.target_language`. Registration returns an access
token and sets the refresh cookie but does not create `UserLanguage`.

The current frontend registration form does not send target language. Onboarding then:

1. Loads the operator-enabled language set.
2. Filters the frontend catalog.
3. Selects `en-GB` by default unless a valid query choice is provided.
4. Collects optional learning goals.
5. Sends language and goals through `PATCH /api/auth/me`.
6. Creates or activates the initial `UserLanguage`.
7. Navigates to Dashboard; assessment remains a separate next action.

The learning-goals subtitle identifies the selected language using the localized `targetLanguages`
ISO 639-1 entry rather than the regional selector label. The name appears as a standalone language
label, so translations do not require language-specific articles or inflections. Unrecognized
selection codes use the language of `DEFAULT_TARGET_LANGUAGE` (`en-GB`) for display, including while
the available-language request is pending or has failed. This display fallback does not change the
selected code or replace backend validation.

## Compatibility field

`users.target_language` remains part of registration and profile responses for defaults and older
flows. It is not the authority for authenticated active-learning context.

- `PATCH /api/auth/me` updates it and synchronizes a `UserLanguage`.
- `PUT /api/languages/active` updates it on explicit language switch.
- Active application context comes from `UserLanguage.is_active`.
- Resource-owned context comes from `StudyPlan.target_language`.

New code must not infer a plan-owned operation's language from the compatibility field.

## Regional and writing-system behavior

Prompt builders receive an explicit target-language name and shared overlay. Current overlays specify
British/American English, Spanish from Spain, European Portuguese, French from France, German from
Germany, standard Italian, Japanese kanji/kana, South Korean Hangul, and Mainland Mandarin with
simplified characters.

Chat, voice, assessment, lessons, flashcards, Listening, and Reading consume these instructions where
their prompt builders require them. There is no legacy `american`/`british` conversion contract.

Comprehension length guidance uses characters for Japanese and Mainland Chinese and words for the
other current languages.

## Speech recognition

Speech providers require ISO 639-1. `get_iso639()` maps canonical BCP-47 codes and falls back to the
lowercase prefix for unknown codes.

Generic `POST /api/stt` requires a user-owned `study_plan_id`, derives language from that plan, and
always passes ISO explicitly. Voice conversation passes the resolved session language. There is no
implicit English default inside either STT adapter.

TTS currently accepts but ignores a language argument; regional speech output depends on configured
provider voice rather than automatic target-language selection.

## Validation boundaries

- Registration and profile update validate supported target languages.
- Add and switch validate operator-enabled target languages.
- Several static-resource language queries rely on dispatcher fallback instead of allow-list rejection.
- Voice WebSocket language input is not uniformly validated and can use fallback plan resolution.
- Exact regional variants remain distinct pool/cache keys where features scope by BCP-47 code.

## Related specifications

- `multi-language.instructions.md` — ownership, active selection, isolation, and lifecycle.
- `add-target-language.instructions.md` — implementation checklist for another language.
- `learning-resources.instructions.md` — canonical language datasets.
- `speech-services.instructions.md` — provider contracts.
- `prompts.instructions.md` — language overlays and prompt composition.
