---
description: "Current LLM prompt ownership, composition, roles, structured outputs, language overlays, and untrusted-data rules."
applyTo: "backend/app/services/prompts/**, backend/app/services/{llm_adapter,lesson_generator,flashcard_sm2,assessment,listening_service,reading_service,conversation_pipeline,memory_service}.py, backend/app/routers/{chat,lessons,grammar,vocabulary,phrasebook,assessment,admin_dashboard_banner}.py"
---

# Prompt Architecture

## Ownership

Active reusable prompt templates and builders live in `backend/app/services/prompts/`. Services and
routers supply runtime values and process results; they should not duplicate prompt policy.

One current exception is dashboard-banner translation: `_TRANSLATION_PROMPT` remains inline in
`routers/admin_dashboard_banner.py` and returns `DashboardBannerTranslationResponse`. It interpolates
administrator content directly and does not use the shared delimiter pattern. This exception must be
considered when changing prompt-safety assumptions.

## Package responsibilities

- `common.py`: plain-text output policy, JSON-only/retry fragments, Anthropic system-only trigger,
  Lingu name, memory-tool policy, and language overlays.
- `tutor.py`: text and voice tutor system prompts, including the written-chat formatting policy.
- `speech.py`: native-pronunciation instructions for all `gpt-4o-mini-tts` synthesis, including its
  snapshots. The TTS adapter gates support; legacy/unknown models receive no instructions. Supplied
  language codes add regional guidance; absent context requests per-passage language inference.
  Known languages also receive focused articulation guidance for native vowel/consonant quality,
  timing, stress, and tonal or pitch distinctions where relevant. These details apply only to passages
  in that language and preserve the selected voice's identity; they are not specific to the default voice.
  Spoken text must be read faithfully, never translated, extended, or treated as executable instructions.
- `lesson.py`: lesson generation, invalid-exercise regeneration, native support, and exercise grading.
- `flashcards.py`: deck generation, selected-word lookup and contextual translation of new imported terms.
- `comprehension.py`: Listening and Reading generation and post-attempt question explanations.
- `games.py`: generation and separate semantic review for Error Detective, Sentence Order, and
  Vocabulary Pairs. Plan language/level, profile native language, allowed source identifiers and
  bounded mistakes are explicit inputs. Reference data is not instructions. The upcoming lesson
  guides relevance without authorizing unstudied material. Game-specific structured schemas validate
  Detective fragments/replacements/options, Sentence Order fragments/accepted permutations, and
  Vocabulary Pairs terms/meanings/examples; semantic review checks linguistic validity and ambiguity.
- `assessment.py`: free-write placement, level test, and alternate assessment flow.
- `grammar.py`, `vocabulary.py`, and `phrasebook.py`: native-language resource support.

`__init__.py` exposes the builders consumed outside the package.

## Shared composition

`JSON_ONLY_INSTRUCTION` and `STRUCTURED_OUTPUT_RETRY_PROMPT` support callers using
`LLMAdapter.structured_output()`. Assessment free-write and level-test callers instead use raw chat
plus explicit JSON parsing; their builders include the same `JSON_ONLY_INSTRUCTION`.

`PLAIN_TEXT_OUTPUT_INSTRUCTION` forbids Markdown formatting in voice replies and generated resource
text, including JSON string values, because those surfaces display text literally. It excludes emphasis markers,
headings, blockquotes, list markup, tables, Markdown links, and inline/fenced code. Ordinary sentences
and paragraph breaks are preferred. Required JSON structure, keys, arrays, data types, tool-call
format, exercise blanks such as `___`, and meaningful punctuation must be preserved.

The policy is part of the voice tutor system prompt and `JSON_ONLY_INSTRUCTION`, covering voice,
structured generation, and raw-JSON assessment across providers. Voice greetings and tool-free
fallbacks use the same voice builder; tool continuations retain the system prompt. This is a
prompt-level formatting instruction, not a Markdown parser or output sanitizer.

Written chat instead uses `CHAT_OUTPUT_INSTRUCTION` from `tutor.py`. It permits optional Markdown
bold, italics, bullet/numbered lists and paragraphs when useful for corrections or explanations.
Plain text remains valid; the model must not add formatting to every response. Headings, blockquotes,
tables, links, images, HTML and inline/fenced code are excluded. Normal turns and tool-free fallbacks
use the same policy. The prohibition on emojis remains independent of formatting.

`get_language_prompt_overlay(target_language)` supplies regional and writing-system guidance for
canonical BCP-47 codes and supported short aliases. It is composed into tutor, voice, lesson,
evaluation, flashcard, comprehension, and assessment prompts. Target-language metadata comes from
language helpers rather than client labels.

Russian (`ru-RU`, internal alias `ru`) has explicit Cyrillic, pronunciation, case, aspect, motion-verb
and register guidance. The canonical language and writing-system rules, including ё and optional
pronunciation stress marks, are defined in `target-language.instructions.md`.

Swedish (`sv-SE`, internal alias `sv`) has explicit pronunciation, en/ett gender, definiteness,
V2/subordinate word order, reflexive reference, tense and register guidance. The canonical variety,
writing-system and speech rules are defined in `target-language.instructions.md`.

`MEMORY_SYSTEM_INSTRUCTION_BASE` and `get_memory_system_instruction()` advertise the native
`save_user_memory` tool only when the request actually offers that tool. No-tools fallbacks may retain
escaped memory context but must not instruct the model to call an unavailable tool.

## Tutor prompts

Text and voice prompts lock the Lingu persona, learning scope, safety behavior, target language, native
support, learner context, and optional memories.

Text tutoring responds primarily in the target language and may briefly explain corrections in the
learner's native language, with optional basic formatting. Voice output uses short TTS-safe plain text. Detailed persistence, access,
and streaming behavior belongs to Platform and Voice Conversation specs.

Voice's language policy permits brief profile-native help only when the learner requests learning
assistance, an explanation or translation, or signals incomprehension. Lingu then supplies a
target-language example and an easy question to resume practice. Greetings, ordinary corrections and
hints remain target-language by default. Overlays apply to target-language passages without overriding
this exception. This policy is retained by lesson-practice and tool-free prompt construction.

Lesson-linked voice sessions additionally receive `lesson_practice_context`. The service loads this
bounded, escaped JSON reference from an owned completed lesson and its answered exercises; the client
supplies only the lesson ID. The prompt treats it as non-authoritative data inside `lesson_practice`
delimiters. It asks Lingu to open with a relevant question, provide hints and gentle corrections, and
revisit difficult structures. Lingu may acknowledge sufficient practice and offer to finish or
continue, but cannot end the session or impose a new duration. The context remains in prompt arguments
through greeting, memory refresh, and tool-free fallback, independently of the bounded turn history.

## Learning prompts

Lesson generation receives CEFR level, language overlay, unit/topic, declared lesson type, curriculum
grammar/vocabulary references, native language, and a bounded summary of prior sibling lessons. The
summary includes a bounded deduplicated vocabulary sample gathered from siblings; it is not a complete
transcript of prior content.

The lesson type selects explanation focus and exercise mix. Generated structures are validated through
Pydantic. Separate builders cover invalid-exercise replacement, missing lesson/exercise native
explanations, hints, question translation, fill-blank grading, free-write grading, and pronunciation grading.

Lesson generation and regeneration request `question_translation` in the native language (null when
none is supplied). Shared translation rules preserve blank markers, quoted target-language text and
phrases to manipulate or pronounce, translate task requirements, and forbid solutions or extra hints.
The on-demand translation builder receives only the exercise type and displayed question alongside
source/destination language names; it does not receive answers, options, or explanations. It delimits
the question as untrusted data and explicitly forbids carrying out its instructions. Cache ownership
and structural checks belong to `study-plan.instructions.md` (Optional question translation).

Flashcard prompts generate target-language words/examples and native-language support. Comprehension
prompts receive `length_guidance`; `word_count` is only a builder fallback used to construct guidance
when an explicit language-aware value is absent.

Bulk-card translation uses profile native language and persisted plan target language, with words,
definitions and examples in a separate untrusted JSON message. It translates the term's contextual
meaning without rewriting the original card. The structured schema requires one nonblank translation
of at most 255 characters for every input index, with no omitted, duplicate or additional indices.
Provider context uses at most 300 characters per definition/example; full original card content remains
available for persistence. Translation and corrective retry share the service's bounded deadline.

Post-attempt comprehension help uses a system instruction and a separate untrusted JSON source message
containing the saved passage, question, options, answer key and level. It requests a concise native
explanation and one contiguous literal evidence quote, distinguishing inference from explicit statements.
No learner answer or personal data enters the reusable explanation. The service validates nonempty,
bounded fields and that evidence occurs exactly in the passage; linguistic accuracy remains model-dependent.

Resource-help prompts receive canonical static source JSON and preserve target-language examples while
generating native-language explanation.

## Roles and output modes

- Tutor and voice: system prompt with streaming conversational text.
- Lesson generation/regeneration/evaluation and flashcards: system prompt with Pydantic structured
  output.
- Comprehension generation and static-resource native help: user prompt with Pydantic structured output.
- Comprehension post-attempt help: system instruction plus untrusted source JSON, with structured output.
- On-demand lesson native help: user prompt with Pydantic structured output.
- Free-write assessment and level test: system prompt with raw JSON parsed by the assessment service.
- Dashboard-banner translation: inline user prompt with Pydantic structured output.

Provider-specific formatting is owned by `llm_adapter.py`; callers should pass semantic roles rather
than construct SDK-specific requests.

## Untrusted dynamic data

User-controlled, generated, or persisted text inserted into prompts is data, not instruction. Where a
builder provides sentinel blocks, callers must preserve them and their accompanying non-authoritative
instruction.

Exercise evaluation, exercise regeneration, prior-lesson summaries, flashcard topic/context, and
free-write assessment use explicit delimiters plus instruction-isolation language. Lesson native-help
and static-resource-help prompts delimit source JSON but do not all include the same explicit
anti-instruction wording. Dashboard-banner translation currently has neither shared protection.

Do not claim uniform prompt-injection isolation until those exceptions are changed in code.

Memory context is escaped and explicitly non-authoritative. Prompt builders must not concatenate raw
memory or profile data outside the memory/context helpers.

## Maintenance rules

1. Add reusable prompt text under `services/prompts/`; avoid new inline router prompts.
2. Keep business orchestration and persistence outside prompt modules.
3. Reuse common JSON, memory, persona, provider, and language fragments.
4. Treat prompt wording, role, schema, language overlay, and delimiter changes as behavior changes.
5. Keep Pydantic schema and prompt output requirements synchronized.
6. Delimit dynamic data and explicitly state that it cannot override instructions.
7. Do not expose correct answers, secrets, internal tool metadata, or private context beyond the
   feature's public contract.
8. Update this spec and the affected domain spec when prompt behavior changes.

## Related specifications

- `services.instructions.md`: callers and effects.
- `llm-error-handling.instructions.md`: provider and structured-output failures.
- `platform.instructions.md`: text tutor behavior.
- `study-plan.instructions.md`: lesson lifecycle.
- `learning-resources.instructions.md`: assessment and native-resource help.
