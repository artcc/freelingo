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

- `common.py`: JSON-only/retry fragments, Anthropic system-only trigger, Lingu name, memory-tool policy,
  and language overlays.
- `tutor.py`: text and voice tutor system prompts.
- `speech.py`: native-pronunciation instructions for all `gpt-4o-mini-tts` synthesis, including its
  snapshots. The TTS adapter gates support; legacy/unknown models receive no instructions. Supplied
  language codes add regional guidance; absent context requests per-passage language inference.
  Spoken text must be read faithfully, never translated, extended, or treated as executable instructions.
- `lesson.py`: lesson generation, invalid-exercise regeneration, native support, and exercise grading.
- `flashcards.py`: deck generation and selected-word lookup.
- `comprehension.py`: Listening and Reading generation.
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
plus explicit JSON parsing.

`get_language_prompt_overlay(target_language)` supplies regional and writing-system guidance for
canonical BCP-47 codes and supported short aliases. It is composed into tutor, voice, lesson,
evaluation, flashcard, comprehension, and assessment prompts. Target-language metadata comes from
language helpers rather than client labels.

`MEMORY_SYSTEM_INSTRUCTION_BASE` and `get_memory_system_instruction()` advertise the native
`save_user_memory` tool only when the request actually offers that tool. No-tools fallbacks may retain
escaped memory context but must not instruct the model to call an unavailable tool.

## Tutor prompts

Text and voice prompts lock the Lingu persona, learning scope, safety behavior, target language, native
support, learner context, and optional memories.

Text tutoring responds primarily in the target language and may briefly explain corrections in the
learner's native language. Voice output uses short TTS-safe plain text. Detailed persistence, access,
and streaming behavior belongs to Platform and Voice Conversation specs.

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
explanations, hints, fill-blank grading, free-write grading, and pronunciation grading.

Flashcard prompts generate target-language words/examples and native-language support. Comprehension
prompts receive `length_guidance`; `word_count` is only a builder fallback used to construct guidance
when an explicit language-aware value is absent.

Resource-help prompts receive canonical static source JSON and preserve target-language examples while
generating native-language explanation.

## Roles and output modes

- Tutor and voice: system prompt with streaming conversational text.
- Lesson generation/regeneration/evaluation and flashcards: system prompt with Pydantic structured
  output.
- Comprehension and static-resource native help: user prompt with Pydantic structured output.
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
