---
description: "Canonical implementation checklist and completion gates for adding interface locales and user native languages, including catalogs, account flows, generated help, emails, announcements, speech, compatibility, and validation."
applyTo: "messages/**, frontend/src/{app,components,hooks,i18n,lib,store}/**, frontend/src/middleware.ts, frontend/tests/**, backend/app/{schemas,models,routers,services,templates/email}/**, backend/tests/**"
---

# Add Interface or Native Language

## Purpose and completion rule

This is the canonical implementation procedure for adding a user interface locale, a user native
language, or both. It complements [Add Target Language](add-target-language.instructions.md);
adding an interface/native language does not require a curriculum or activate a study language.

A language is complete only when every surface belonging to its requested role is implemented,
existing data remains readable, applicable registrations agree, and the required verification has
been performed. An allow-list entry, a translated JSON file, or an English fallback alone is not
completion. Report unverified capabilities and remaining work explicitly.

This guide owns the addition workflow. [Platform](platform.instructions.md#language-roles-and-internationalization)
owns account language roles and locale resolution. Domain specifications remain authoritative for
their behavior; reference them rather than duplicating their contracts in a new language-specific spec.

## 1. Establish the requested scope

Identify the requested language, canonical code, intended regional variety, writing system, and role:

- **Interface:** controls, navigation, accessible labels, public pages, account flows, administration,
  announcements, and tour narration. This uses `ui_locale` and the rendered request locale.
- **Native:** pedagogical explanations, translations, learner support, generated memories, native
  feedback/titles, and account email. This uses `native_language`.
- **Both:** complete both paths. Their supported sets currently coincide, but they are independent
  preferences and must not be treated as one field.
- **Study language:** a separate request governed by `add-target-language.instructions.md`.

For a native-only addition, translate its name in existing UI catalogs and complete native consumers;
do not create an entire new interface catalog unless interface support is also requested. For a
UI-only addition, complete interface consumers without silently registering another native language.
Review tests and selectors that currently assume the two supported sets are equal.

Do not add target-language packages, flags, learning overlays, `SUPPORTED_TARGET_LANGUAGES`, or
`AVAILABLE_TARGET_LANGUAGES` merely because a native/UI language is being added. Conversely, a new UI
catalog must translate the labels of all existing study languages without changing their inventory.

Keep the existing account, authorization, resource ownership, learning progress, and quota boundaries.
An existing study language with the same base code is not evidence that the interface or native
support is complete.

## 2. Inspect current registrations and choose the code

Read the relevant code and local instructions before editing. Use the paths below as an inventory,
then search for the current constants, codes, dictionaries, explicit language counts, and hard-coded
test arrays to find additional consumers. Reconcile any moved files with their current equivalents.
Do not assume that this checklist replaces code discovery.

The current application uses short, lowercase language codes for UI/native preferences and regional
BCP-47 codes for study languages. Account validators use exact allow-list membership; they are not a
general BCP-47 normalizer.

Before introducing regional variants, script subtags, or longer language codes, inspect:

- `backend/app/schemas/auth.py` and `schemas/admin.py`: native/profile locale input limits currently
  allow at most five characters.
- `backend/app/models/user.py`: native and UI columns currently use `String(10)`.
- `backend/app/models/dashboard_banner.py`: `source_locale` currently uses `String(2)`.
- `frontend/src/middleware.ts` and the initial browser script in `app/layout.tsx`: browser negotiation
  currently reduces language tags to their base language.
- Speech aliases, Open Graph mappings, cache identities, persisted language fields, and tests.

Define canonical spelling and regional fallback behavior before exposing a variant; do not collapse
distinct requested variants through the existing base-language resolver. If storage changes are
needed, commit a versioned Alembic revision following the existing chain. Adding another compatible
short code does not by itself require a database migration. Database execution requires separate
authorization under the project rules.

Specify the editorial variety explicitly where a short code is ambiguous. Check consistency between
the translated text, native-language prompt names, speech pronunciation, dates, and social metadata;
do not infer region from an unrelated target-language mapping or reporting country estimate.

## 3. Register the applicable role

### Interface registrations

- `frontend/src/lib/locales.ts`: `SUPPORTED_LOCALES` and its derived type.
- `frontend/src/app/layout.tsx`: initial browser detection inventory.
- `frontend/src/middleware.ts` and `src/i18n/request.ts`: negotiation, request forwarding, and catalog
  resolution. A new short code normally reuses these algorithms; variants require explicit review.
- `frontend/src/components/settings/ProfileSection.tsx`: interface options and save behavior.
- `backend/app/schemas/auth.py`: `SUPPORTED_UI_LOCALES`.
- `frontend/src/lib/seo.ts`: `OPEN_GRAPH_LOCALES`.
- Announcement registrations described below.

### Native-language registrations

- `backend/app/schemas/auth.py`: `SUPPORTED_LANGUAGES`, used by registration and profile validation.
- `backend/app/schemas/admin.py`: native-language `SUPPORTED_LANGUAGES` for administrative creation.
- `frontend/src/app/(auth)/register/page.tsx`: native-language options.
- `frontend/src/components/settings/ProfileSection.tsx`: native-language options.
- `frontend/src/app/(app)/admin/users/page.tsx`: administrative native-language options.
- `backend/app/services/language_helpers.py`: `_NATIVE_LANGUAGE_NAMES`.

Keep backend and frontend inventories aligned for each role. Public registration, profile updates,
and administrative creation must agree on supported native codes. UI registration must agree with
catalogs, interface selectors, announcements, and tour validation.

Reuse existing shared constants where available. If eliminating duplication, keep UI and native
inventories conceptually separate and preserve their respective consumers. Do not require an
unrelated localization-framework rewrite to add a language.

## 4. Author complete interface catalogs

The canonical catalogs are `messages/<locale>.json` at repository root. Use the current English
catalog as a structural reference and existing translations as editorial context, not as text to
copy unchanged. Preserve the complete current nested key structure, value types, interpolation
arguments, and supported rich-text tags.

Cover the whole product, including public landing/FAQ, legal pages and metadata, cookies, contact,
authentication, onboarding, learning controls, errors, loading/retry/empty states, settings,
billing, administration, accessible descriptions, tour, and current What's New entries. Do not
translate only the learner dashboard.

For every new selectable UI/native code:

- Add its localized name to `languages` in every applicable UI catalog.
- Add announcement-editor locale labels under `admin.dashboardBanner.locales` for UI additions.
- In a new UI catalog, translate all current `targetLanguages` names/descriptions and landing greetings
  while preserving canonical codes and regional distinctions.
- Preserve Lingu's product naming and the editorial rules in
  `architecture-frontend.instructions.md`.

Use complete messages and ICU plural/select forms when grammar depends on values. Preserve semantic
arguments and tags while allowing the plural categories needed by the new locale. Do not implement
plurality as only `count === 1`, or construct inflected sentences by concatenating a phrase with a
standalone language name. Neutral labels with interpolation are preferable when they avoid
language-specific inflection.

Preserve diacritics, punctuation, meaningful spacing, and natural register. Review translated legal
and commercial statements against the current product contract rather than propagating obsolete
claims from another catalog. Identical brand names or technical terms are legitimate; untranslated
prose or placeholder text is not a completed translation.

The runtime import resolves `frontend/messages/`; `frontend/Dockerfile` copies root catalogs there
and `docker-compose.dev.yml` mounts them there. Keep the root directory authoritative, without a
second independently maintained translation tree. Tests that import root catalogs do not establish
that a particular runtime has the catalogs mounted or copied correctly.

Catalog-import failure currently loads English without changing the selected locale. There is no
application-level English merge for individual missing keys. Treat these as recovery limitations,
not permission to ship incomplete catalogs; distinguish fallback verification from language coverage.

## 5. Preserve account and locale behavior

Follow the platform contract for cookie/header negotiation, initial server rendering, and Settings
save/reload behavior. Verify the new language across first visit, registration, login, session
restoration, profile edits, and administrative user creation as applicable.

Current boundaries that an addition must account for:

- Interface resolution defaults to `en`; the registration form initially selects native `es`.
  The form does not infer native language from the interface or send a UI preference.
- Onboarding selects learning language/goals, not interface/native preferences.
- Login and session restoration load the stored `ui_locale` but do not automatically apply it to
  the rendered locale or cookies. Logout retains locale cookies.
- Settings updates `NEXT_LOCALE` and `LOCALE_DETECTED` only after a successful save in the current
  account session, and reloads when the selected UI differs from the rendered locale.
- The current UI has no automatic/reset-to-browser locale option.

Do not silently change account-versus-device precedence, defaults, or synchronization as part of a
language addition. A requested change to those rules needs an explicit behavior decision and tests.
Include unsupported/stale cookies and missing catalogs in the review; do not assume an existing
cookie is valid merely because it is present.

## 6. Complete native-language consumers

### Generated support and deterministic text

`_NATIVE_LANGUAGE_NAMES` supplies a meaningful language name to prompts; otherwise helpers can pass
the raw code through. Verify native context reaches written/voice tutoring, lesson generation and
support, flashcards, grammar/vocabulary/phrasebook help, Listening/Reading explanations, games, and
new automatic memories. Keep target-language exercises and examples in their owning study language.
The prompt modules normally interpolate the native-language name; translating the system prompts
themselves is not required.

Update the deterministic native-language catalogs:

- `backend/app/services/language_helpers.py`: `_VOICE_SESSION_TITLES`,
  `_LESSON_PRACTICE_TITLES`, `_MONTH_NAMES`, and locale-specific date composition where needed.
- `backend/app/routers/lessons.py`: `_ANSWER_FEEDBACK`.

Check natural date order, punctuation and month inflection, not only dictionary presence. Preserve
UTC date behavior and existing title-length limits. English fallbacks must not hide a missing entry
for the newly supported native language.

### Existing content and caches

Changing the profile native language does not perform a global retranslation:

- Grammar, Vocabulary, Phrasebook, and comprehension help use language-aware shared help caches.
- Exercise question translations require matching native language and source text.
- Existing lesson/exercise native explanations and hints can be reused from saved content without
  matching the new profile language.
- Saved flashcards, conversation titles/transcripts, and memories are not automatically rewritten.
- Game sessions retain their captured native language.

Use the owning resource, study-plan, games, memories, and conversation specifications for details.
Preserve resource ownership and cache isolation. Do not relabel historical text as newly translated,
flush all language caches, or promise immediate conversion of existing content. If the requested
scope includes retranslation, define it separately, including provenance, concurrency, cost, and
authorization for any persistent data rewrite.

### Emails and reporting

In `backend/app/services/email_service.py`, complete all seven catalogs:
`_VERIFY_I18N`, `_RESET_I18N`, `_WELCOME_I18N`, `_DELETION_I18N`, `_CONTACT_I18N`,
`_FEEDBACK_I18N`, and `_REVIEW_I18N`.

Account messages use the recipient's native language. Contact, feedback, and review notifications
use the first administrator's native language with English fallback, not the sender's UI. Review
subjects, body, buttons, footer, interpolations, and the shared `backend/app/templates/email/`
templates, including document title, `lang`, escaping, and direction.

The renderer currently resolves the HTML language using `_VERIFY_I18N`; partially extending email
catalogs can therefore mislabel another template's fallback content. Verify content and HTML language
together for every message type. Email links do not currently carry a locale override.

Review `_COUNTRY_ESTIMATES` in `backend/app/services/revenuecat_service.py` when adding a native
language. Follow `subscriptions-freemium.instructions.md`: this is optional reporting metadata, not
verified residence. Explicitly choose a justified mapping or the existing empty estimate; do not
invent a country just to fill the dictionary.

## 7. Complete interface announcements and speech

### Dashboard announcements and What's New

For a new UI locale, coordinate:

- `backend/app/schemas/dashboard_banner.py`: locale literal, stored/read translations, and required
  write/translation-result schemas.
- `backend/app/routers/admin_dashboard_banner.py`: translation prompt's locale inventory/count and
  preservation of source text.
- `frontend/src/app/(app)/admin/system/page.tsx`: editor options, completeness checks, and labels.
- `frontend/src/components/dashboard/DashboardAnnouncement.tsx` and `src/store/config.ts`:
  announcement selection, response types, and missing-translation behavior.

Make the new translation optional when reading older stored banners and required for complete new
writes/translation results. Preserve the existing ability to read incomplete historical maps, edit
them, and complete them without fabricating translations. Adding translated content follows the
normal revision/dismissal rules in `database-models.instructions.md`; it is not an active-state-only
change. Verify the display fallback for an older banner in the newly added UI.

Translate the current What's New entries and retain their version in the new catalog.
`whats-new.instructions.md` governs announcement changes; a new translation alone does not require
re-announcing old entries or changing `WHATS_NEW_VERSION`.

### Tour narration and native-language speech

The tour speaks the interface language independently of native and learning language. Review:

- `backend/app/routers/tts.py`: UI-locale validation for tour requests.
- `backend/app/services/tour_audio.py`: language-aware text/configuration cache identity.
- `backend/app/services/prompts/speech.py`: `_SPEECH_LANGUAGES` and
  `_PRONUNCIATION_GUIDANCE` together; a recognized language must have its required guidance.
- `backend/app/services/gemini_tts_service.py`: short UI-to-regional aliases.
- Frontend tour/proxy behavior and the translated tour text.

Check support for the configured provider/model and intended pronunciation using applicable provider
documentation. Also consider native-language support spoken during voice tutoring when adding a
native language. A voice-selection preview in English does not verify either capability.

The current Kokoro voice configuration is English-only. Do not claim that registering a locale makes
all providers support its speech, or silently switch deployment providers. Follow
`speech-services.instructions.md` for capability limits, caching, and recoverable failures.
Native/UI additions do not change resource-owned STT: recognition still derives from the owned study
plan and uses its explicit language.

## 8. Review presentation, accessibility, and public metadata

For every addition, review:

- Unicode glyph coverage, line wrapping, text expansion, readable sizes, and mobile controls.
- Explicit `lang` for native help when it differs from the UI; mixed target/native text must retain
  its actual language. Reuse the established components and text semantics.
- Accessible names and label associations for selectors, dialogs, errors, and narration controls.
- Sorting using the rendered locale's collation, and dates, numbers, lists, and prices using the
  appropriate UI/native locale rather than the host default.

For right-to-left languages, implement and review direction metadata, document/content `dir`,
logical layout properties, mixed-direction text, focus/navigation, and email layout. Existing
`dir="auto"` on some help blocks is not whole-application RTL support.

For CJK or another newly introduced UI/native script, verify suitable interface and help fonts.
Existing CJK `TargetLanguageText` capabilities apply to learned-language content; importing those
fonts alone does not configure a new interface. Preserve the project's typography and visual system.
Do not declare visual compatibility solely from unit tests.

For UI additions, translate public metadata and register the intended Open Graph locale. Follow
`seo.instructions.md`: current interface variants share canonical URLs; adding a locale does not
create localized routes, sitemap entries, or `hreflang`. Such indexing changes require a separate
architecture decision.

`docs/index.html` is an independent English project overview under `public-site.instructions.md`.
It does not require a translated copy for every UI/native addition. Public study-language lists and
language bubbles still describe study languages, not the new native/interface inventory.

## 9. Verification and completion gates

Add or extend focused tests for the affected role using the existing pytest/Vitest infrastructure.
Do not assume that current namespace-specific tests cover the entire new language. Required coverage:

- **Registrations:** applicable backend/frontend sets, selector options, localized names, and catalog
  files agree; administrative and public native acceptance match. Rejection tests use otherwise valid
  payloads so an unrelated error cannot mask missing language validation.
- **Catalogs:** recursive key/value-shape parity, nonempty messages, matching semantic interpolation
  arguments and rich-text tags, and successful ICU rendering. Exercise locale-relevant plural
  categories, zero, and representative compound numbers, allowing legitimate category differences.
  Keep technical keys, brand names, and deliberately invariant values intact.
- **UI lifecycle:** supported cookie/header/browser detection, precedence, first server render,
  unsupported input and fallback, successful/failed Settings saves, reload behavior, and independence
  from native/target selection. Cover any modified account synchronization or variant negotiation.
- **Native consumers:** meaningful prompt language, deterministic feedback, titles/dates, and
  language isolation for generated help. Test changing native preference with existing content,
  including preserved history and language-aware cache misses.
- **Emails:** every template in the new native language, fallback, correct HTML language, substitutions,
  and escaping.
- **Announcements:** complete new writes, translation preview/source preservation, older stored maps,
  missing-locale display, and revision behavior.
- **Speech:** new UI tour locale accepted, unsupported locale rejected, required aliases/guidance
  present, and cache identities distinct where languages/variants differ. Mock providers in tests.
- **Public presentation:** new UI metadata, legal/landing catalogs, and current What's New key/version
  consistency. Include meaningful accessibility assertions for changed selectors/content.

Find relevant existing tests under `frontend/tests/i18n/`, `tests/middleware.test.ts`,
`tests/components/ProfileSection.test.tsx`, and `tests/seo.test.ts`; backend starting points include
`test_auth.py`, `test_admin.py`, `test_email_service.py`, `test_dashboard_banner.py`,
`test_tour_audio.py`, `test_prompts.py`, `test_conversation.py`, and `test_lesson_voice_practice.py`.
Search for further affected tests and manual locale arrays rather than treating this list as exhaustive.

Use `testing.instructions.md` and the repository-local runner. Obtain approval before tests,
formatters, lint, typechecks, builds, container startup, or application checks; start with the smallest
relevant set. Stop and report a failed test before modifying code or tests. Never contact real
providers from automated tests.

Structural checks cannot establish idiomatic translation, correct legal meaning, visual accessibility,
or speech quality. Include linguistic review and authorized browser/email/audio checks as applicable;
report any pending review explicitly. Re-read the final diff for omitted registrations, accidental
target-language changes, and English fallbacks masking incomplete support.

## 10. Documentation and delivery

Before editing documentation, identify the exact affected files and obtain approval. Normally review:

- `platform.instructions.md`: supported interface/native roles and account behavior.
- `architecture-frontend.instructions.md`: localization structure and presentation.
- `api-endpoints.instructions.md`: accepted codes and announcement contracts.
- `database-models.instructions.md`: announcement completeness and any actual schema changes.
- `speech-services.instructions.md`, `services.instructions.md`, and
  `voice-conversation.instructions.md`: affected speech, email, and title behavior.
- `seo.instructions.md`, `public-site.instructions.md`, `whats-new.instructions.md`, and
  `version.md`: any current locale inventories or statements affected by an addition.
- `subscriptions-freemium.instructions.md`: changes to the country-estimate convention.

Update prompts, learning-domain, testing, Docker, README, or other specifications only when their
contracts or project summaries change. Testing documentation does not need an inventory of every
new language test. Keep this guide central and update it if implementation responsibilities move;
do not distribute copies of its checklist across other specs.

Ask whether an unreleased user-visible addition warrants a `CHANGELOG.md` entry. Follow the version
and What's New workflows only when the corresponding change is approved. A guide-only edit does not
itself add language availability.

Conclude with the implemented role/code, completed surfaces, actual verification, remaining provider
or review limitations, and any required schema/deployment coordination. Keep validation results and
release history out of this specification.
