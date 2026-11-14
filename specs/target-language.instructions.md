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

The application recognizes 20 study languages, counting each regional variant separately:
`en-GB`, `en-US`, `cs-CZ`, `da-DK`, `de-DE`, `es-ES`, `fi-FI`, `fr-FR`, `hr-HR`, `it-IT`, `nl-NL`,
`pl-PL`, `pt-BR`, `pt-PT`, `ja-JP`, `ko-KR`, `ro-RO`, `ru-RU`, `sv-SE`, and `zh-CN`.

Backend `SUPPORTED_TARGET_LANGUAGES` and the frontend catalog must represent the same canonical set.
Validated account flows compare exact canonical strings; there is no general backend BCP-47 parser or
canonicalizer.

`AVAILABLE_TARGET_LANGUAGES` is the operator-enabled subset. Language-management and onboarding
surfaces expose the intersection of configured available codes and supported implementation.
Registration schema validation uses the supported set, while authenticated add/switch operations use
the available set. Assessment completion and explicit study-plan generation also validate their
resolved language against the available set before curriculum dispatch or persistence, including
session, active-language and profile fallbacks. Unknown,
noncanonical, empty, and disabled codes return `422`.

## Default and fallback

`en-GB` is the application default and general runtime fallback for registration schema, ORM values,
study plans, chat/conversation fallback, frontend metadata, and static-resource dispatchers.
`en-US` is supported but must not be introduced as a new application fallback.

Static curriculum, Grammar, Vocabulary, Phrasebook, and assessment dispatchers currently fall back to
`en-GB` for unknown inputs rather than rejecting them. Validated product flows should still reject
unsupported codes before dispatch.

The Alembic-managed schema defines `en-US` server defaults for `users.target_language` and
`study_plans.target_language`. Application creation paths provide `en-GB` through schema/ORM defaults;
direct inserts relying only on those server defaults are not the supported application path.

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
British/American English, Spanish from Spain, Brazilian and European Portuguese, French from France, German from
Germany, standard Italian, standard Dutch from the Netherlands, standard Polish, contemporary Russian in Cyrillic, Japanese kanji/kana, South Korean Hangul, and Mainland
Mandarin with simplified characters, standard Swedish from Sweden, standard Danish from Denmark,
standard Czech from Czechia, standard Croatian from Croatia, standard Finnish from Finland, and
standard Romanian from Romania.

Chat, voice, assessment, lessons, flashcards, Listening, and Reading consume these instructions where
their prompt builders require them. There is no legacy `american`/`british` conversion contract.

`pt-BR` resolves before the `pt` prefix in every static dispatcher and speech instruction lookup.
The short `pt` alias continues to identify Portugal where regional guidance is needed. Both Portuguese
variants map to ISO `pt` for recognition, but retain distinct BCP-47 learning, pool, and audio-cache keys.
Regional overlay content lives in the prompt builders; curriculum and reference content live in the
language packages. Their common authoring requirements belong to `learning-resources.instructions.md`.
Every package follows the canonical [per-level coverage bounds](learning-resources.instructions.md#per-level-coverage-bounds)
for curriculum units, grammar topics, vocabulary entries, phrases and placement questions. Minimums
apply independently to A1-C2; upper values trigger editorial review rather than automatic truncation.
Regional packages are counted separately and retain their own syllabus and progression.

`nl-NL` resolves to the independent `backend/app/data/nl/` package; `nl` is its internal dispatcher and
prompt alias, not an accepted account target code. Dutch content uses Netherlands usage while
recognizing valid standard variants. It uses Latin text, word-based comprehension lengths, ISO `nl`
recognition, and the Netherlands flag. Shared speech guidance requests Netherlands pronunciation.

`ru-RU` resolves to the independent `backend/app/data/ru/` package; `ru` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Russian uses Cyrillic, visible word
spacing, word-based comprehension lengths, ISO `ru` recognition and the Russian flag. Romanization is
not required. Its curriculum introduces Cyrillic and pronunciation before progressing through cases,
aspect, motion verbs and advanced discourse. Generated content uses contemporary standard Russian,
preserves appropriate ё spelling and distinguishes contextual alternatives from grammatical errors.
Shared speech guidance requests Russian lexical stress, vowel reduction and hard/soft consonants.

`sv-SE` resolves to the independent `backend/app/data/sv/` package; `sv` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Swedish uses Latin text with å, ä
and ö, visible word spacing, word-based comprehension lengths, ISO `sv` recognition and the Sweden
flag. Its curriculum introduces pronunciation and vowel-consonant length, en/ett gender and
definiteness before subordinate word order, tense perspective and advanced discourse. Generated
content preserves V2, negation scope, reflexive reference and register without rejecting valid regional
or conversational alternatives. Shared speech guidance requests Swedish vowel quality, length
contrasts, pitch accents and natural phrasing. OpenAI speech and Whisper support Swedish; the
English-only Kokoro voice configuration is not suitable for this target language.

`da-DK` resolves to the independent `backend/app/data/da/` package; `da` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Danish uses Latin text with æ, ø
and å, visible word spacing, word-based comprehension lengths, ISO `da` recognition and the Denmark
flag. Its curriculum introduces pronunciation, en/et gender and definiteness before subordinate word
order and advanced discourse. Generated content distinguishes Danish definiteness from Swedish double
definiteness and preserves V2, negation scope, reflexive reference and register. Shared speech guidance
requests Danish vowels, soft d, natural reductions and stød where appropriate without treating regional
pronunciation as an error. OpenAI TTS, Gemini TTS and Whisper support Danish; the English-only Kokoro
voice configuration is not suitable for this target language.

`cs-CZ` resolves to the independent `backend/app/data/cs/` package; `cs` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Czech uses Latin text with Czech
diacritics, visible word spacing, word-based comprehension lengths, ISO `cs` recognition and the Czech
Republic flag. Its curriculum introduces spelling, vowel length and stress before gender, animacy,
cases, aspect, motion verbs, clitics and advanced discourse. Generated content preserves Czech
diacritics and distinguishes standard, common spoken and regional usage without substituting Slovak
or Polish. Shared speech guidance requests vowel length independently of stress, ř, palatal
consonants, syllabic r/l and natural voicing assimilation. OpenAI TTS, Gemini TTS and Whisper support
Czech; the English-only Kokoro voice configuration is not suitable for this target language.

`hr-HR` resolves to the independent `backend/app/data/hr/` package; `hr` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Croatian uses Latin text with
č, ć, đ, š and ž, the digraphs dž, lj and nj, standard ijekavian spelling, visible word spacing,
word-based comprehension lengths, ISO `hr` recognition and the Croatia flag. Its curriculum develops
spelling and pronunciation before gender, animacy, cases, aspect, clitics and advanced interaction.
Generated content distinguishes standard, regional and conversational usage, preserves participants
and certainty in reformulations, and does not substitute neighbouring language conventions. Shared
speech guidance requests Croatian consonant contrasts, syllabic r, natural lexical accent, vowel
length and ijekavian pronunciation. OpenAI TTS, Gemini TTS and Whisper support Croatian; the
English-only Kokoro voice configuration is not suitable for this target language.

`fi-FI` resolves to the independent `backend/app/data/fi/` package; `fi` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Finnish uses Latin text with ä and ö,
visible word spacing, word-based comprehension lengths, ISO `fi` recognition and the Finland flag.
Its curriculum develops vowel and consonant length, vowel harmony and consonant gradation before
extended case, object, verb and discourse contrasts. Generated content distinguishes standard written,
spoken and regional Finnish, preserves participants and scope, and teaches partitive versus total
objects through context rather than English tense equivalents. Shared speech guidance requests native
vowel quality, meaningful vowel and consonant length and initial word stress. OpenAI TTS, Gemini
`gemini-3.8-flash-tts` and Whisper support Finnish; Gemini `gemini-3.8-flash-lite-tts` does not list
Finnish support, and the English-only Kokoro voice configuration is not suitable for this target.

`ro-RO` resolves to the independent `backend/app/data/ro/` package; `ro` is its internal dispatcher,
capability and prompt alias, not an accepted account target code. Romanian uses Latin text with
ă, â, î, ș and ț, comma-below ș/ț, visible word spacing, word-based comprehension lengths, ISO `ro`
recognition and the Romania flag. Its curriculum develops spelling, pronunciation, gender, agreement
and suffixed definite articles before extended case, tense, conjunctive, conditional and clitic
contrasts, then advanced interaction and discourse. Generated content uses contemporary Romanian
from Romania, distinguishes standard, regional and conversational usage, and preserves participants,
scope and certainty in reformulations. Shared speech guidance requests Romanian vowel distinctions,
native r and lexical stress. OpenAI TTS, Gemini `gemini-3.8-flash-tts` and
`gemini-3.8-flash-lite-tts`, and Whisper list Romanian support; the English-only Kokoro voice
configuration is not suitable for this target.

Comprehension length guidance uses characters for Japanese and Mainland Chinese and words for the
other current languages, including Croatian, Czech, Danish, Finnish, Polish, Romanian, Russian and Swedish.

## Speech recognition

Speech providers require ISO 639-1. `get_iso639()` maps canonical BCP-47 codes and falls back to the
lowercase prefix for unknown codes.

Generic `POST /api/stt` requires a user-owned `study_plan_id`, derives language from that plan, and
always passes ISO explicitly. Voice conversation passes the resolved session language. There is no
implicit English default inside either STT adapter.

TTS accepts a full BCP-47 language argument. OpenAI `gpt-4o-mini-tts` and its snapshots use it for
native regional pronunciation instructions; without context, instructions request language inference
without imposing a regional accent. Legacy/unknown OpenAI models and Kokoro ignore this argument.
Model and voice selection remain configured independently of the target language. Provider and
resource-owned language contracts are defined in `speech-services.instructions.md`.

## Validation boundaries

- Registration and profile update validate supported target languages.
- Add and switch validate operator-enabled target languages.
- Both plan-creation endpoints validate the resolved operator-enabled code before any curriculum
  lookup or mutation. An explicit empty code is invalid, not an omitted selection.
- Several static-resource language queries rely on dispatcher fallback instead of allow-list rejection.
- Free voice sessions validate the resolved language against the canonical supported set. They only
  associate an owned active plan in that language; resolution and no-plan behavior are defined in
  `voice-conversation.instructions.md`.
- Exact regional variants remain distinct pool/cache keys where features scope by BCP-47 code.

## Related specifications

- `multi-language.instructions.md` — ownership, active selection, isolation, and lifecycle.
- `add-target-language.instructions.md` — implementation checklist for another language.
- `learning-resources.instructions.md` — canonical language datasets.
- `speech-services.instructions.md` — provider contracts.
- `prompts.instructions.md` — language overlays and prompt composition.
