---
description: "Current implementation checklist and quality gates for adding a complete target language without silent English fallback."
applyTo: "backend/app/{data/**,core/config.py,schemas/auth.py,services/{language_helpers,reading_service}.py,services/prompts/common.py}, frontend/{src/{app,components,lib}/**,public/flags/**,tests/**}, messages/**, .env.example, .env.dev"
---

# Add Target Language

## Completion rule

A target language is selectable only after its learning package, dispatchers, metadata, frontend
catalog, assets, UI translations, provider assumptions, and integrity tests are complete. Do not add a
code to `SUPPORTED_TARGET_LANGUAGES` as a placeholder.

Use `backend/app/data/en_GB/` as a structural baseline, not a pedagogical template. Meet the canonical
[per-level coverage bounds](learning-resources.instructions.md#per-level-coverage-bounds) for units,
grammar topics, vocabulary entries, phrases and placement questions. Audit each level separately;
review any upper-threshold excess editorially rather than trimming useful material automatically.
Languages share these coverage criteria without sharing an identical grammatical syllabus.

## Learner-facing language

For a non-English target, learner-facing didactic fields must be written in that target language:

- curriculum titles and competency checklists;
- grammar titles, categories, summaries, explanations, structures, rules, examples, and mistakes;
- vocabulary topics, words, definitions, and examples;
- phrasebook situations, phrases, and contexts;
- assessment questions, options, and reading snippets.

English/ASCII remains appropriate for code, identifiers, slugs, internal enums, module names, and
cross-language technical constants. Translation/support fields must be explicitly named; missing
target content must not silently use English.

## Backend package

Create one package below `backend/app/data/` following existing naming conventions. It must export:

- `CURRICULUM`: A1-C2 units.
- `GRAMMAR_TOPICS`: grammar reference topics.
- `VOCABULARY_SETS`: vocabulary sets.
- `PHRASEBOOK_CATEGORIES`: practical phrase categories.
- `ASSESSMENT_BANK`: placement questions.

Use per-level modules and assembler modules where the package size warrants it. Assemblers should
collect data rather than duplicate content or runtime dispatch behavior.

## Data integrity

Curriculum units require stable level-scoped IDs, valid CEFR level/unit number, target-language title
and competencies, grammar slugs, vocabulary-set IDs, lesson types, default weeks, and prerequisite
links.

Every curriculum grammar slug must exist in that language and every related grammar slug must resolve.
Every vocabulary-set reference must exist, IDs/slugs must be unique within the language, and unit
references should resolve where provided.

Phrasebook register values remain `formal`, `neutral`, or `informal`. Categories should cover practical
situations across CEFR levels.

Assessment questions require stable unique IDs, four unique options, an exact matching correct option,
valid skill/level metadata, and a same-language grammar slug when present. The bank must provide useful
coverage across grammar, vocabulary, reading, and CEFR progression without placeholder content.

## Backend dispatchers

After the package is complete, register it in:

- `backend/app/data/curriculum.py`.
- `backend/app/data/grammar.py`.
- `backend/app/data/vocabulary.py`.
- `backend/app/data/phrasebook.py`.
- `backend/app/data/assessment_bank.py`.

Curriculum registration includes both the package mapping and `_I18N` strings used for generated lesson
and test titles/objectives. Without `_I18N`, plan-facing strings fall back to English.

Unknown dispatcher input continues to fall back to `en-GB`; supported product flows must ensure the
new canonical code resolves explicitly so this fallback cannot hide missing registration.

## Allow-lists and operator configuration

Add the canonical BCP-47 code to `SUPPORTED_TARGET_LANGUAGES` only after dispatcher/data completion.
Add it to default `AVAILABLE_TARGET_LANGUAGES`, `.env.example`, and `.env.dev` only when it should be
operator-visible by default.

Selectable frontend options are the intersection of backend-supported, operator-enabled, and frontend
catalog entries. Frontend metadata alone must not activate a language.

## Language and prompt metadata

Update `language_helpers.py` with:

- prompt/display and self names;
- flag and ISO 639-1 code;
- script and optional romanization;
- visible word-spacing behavior;
- comprehension length unit/guidance;
- short ISO alias where helper dispatch requires it.

Add the regional/writing-system overlay and aliases in `services/prompts/common.py`. Verify every LLM
learning surface receives the intended overlay rather than generic English guidance.

Update Reading `_CULTURAL_TOPICS` and aliases when the language needs its own cultural topic pool.
Verify Listening/Reading length guidance, especially for character-based writing systems.

## Speech compatibility

Verify TTS and STT provider support. Kokoro's configured voices are English-only, so a non-English
target normally requires another TTS provider under the current architecture.

Add/verify the BCP-47-to-ISO recognition mapping. Resource STT must continue to derive language from an
owned study plan and must never gain a provider-level English fallback.

## Frontend metadata and assets

Update `frontend/src/lib/target-languages.ts` with canonical code, localized/self names, ISO code, flag
path, script, romanization, spacing, and learned-text class.

Add the flag asset under `frontend/public/flags/`. If the writing system cannot reuse an existing
capability, also update:

- script/romanization TypeScript unions;
- font imports/configuration in `frontend/src/app/layout.tsx`;
- learned-language utility classes in `frontend/src/app/globals.css`;
- `TargetLanguageText` behavior where needed.

Update `targetLanguages` labels/descriptions and landing greetings consistently in all UI locale
catalogs. UI locale support is independent; adding a learning language does not add a new interface
locale automatically.

Adding an interface locale or user native language follows the separate
[Add Interface or Native Language](add-ui-native-language.instructions.md) checklist. Its catalogs,
account flows, emails, announcements, and native-support requirements do not imply a new learning
package.

## Required test updates

Backend coverage must include:

- allow-list, add/switch/remove, and curriculum resolution;
- grammar, vocabulary, phrasebook, and assessment dispatch without English fallback;
- curriculum/resource cross-reference integrity and uniqueness;
- per-level coverage minimums and prerequisite-first grammar before final consolidation;
- language metadata and prompt overlay/aliases;
- Reading cultural/length behavior where applicable;
- owned-plan STT mapping to the expected ISO code.

Frontend coverage must include:

- catalog metadata, canonical lookup, script/font classes, and default invariants;
- selector filtering and flag rendering;
- language store available/add/switch/remove behavior;
- language bubbles or other UI derived from the supported-language set;
- translation-catalog keys and landing greetings.

Search backend and frontend tests for hard-coded supported-language arrays; update every contract that
intentionally asserts the complete set.

## Validation workflow

Propose the smallest relevant backend data-integrity/dispatcher tests and frontend catalog/selector
tests first. Obtain explicit approval before running tests, static checks, formatting, or the full
pre-push workflow. Do not record run results or test counts in this spec.

## Documentation

Always review and request approval for affected documentation. Normally affected:

- `target-language.instructions.md`.
- `multi-language.instructions.md`.
- `learning-resources.instructions.md`.
- `CHANGELOG.md` for user-visible availability.

Conditionally update speech, prompts, services, Docker, API, architecture, README, AGENTS, and version
documents only when their public contracts or project-wide summaries change. Testing documentation
changes only when testing architecture or policy changes, not merely because language-specific tests
were added.
