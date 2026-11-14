"""Shared prompt fragments used across LLM-backed services."""

PLAIN_TEXT_OUTPUT_INSTRUCTION = (
    "OUTPUT FORMAT: The interface displays text literally and does not render Markdown. "
    "Use plain text for all learner-facing content, including text inside JSON string values. "
    "Do not add Markdown formatting: bold or italic markers, headings, blockquotes, "
    "bullet or numbered list markup, tables, Markdown links, or inline/fenced code. "
    "Use ordinary sentences and paragraph breaks instead. "
    "Preserve the requested JSON structure, keys, arrays, data types, and tool-call format. "
    "Keep required exercise markers such as ___ and meaningful punctuation unchanged."
)

JSON_ONLY_INSTRUCTION = (
    "IMPORTANT: Respond with ONLY a valid JSON object. "
    "No markdown, no code fences, no extra text. " + PLAIN_TEXT_OUTPUT_INSTRUCTION
)

STRUCTURED_OUTPUT_RETRY_PROMPT = (
    "That response was not valid JSON. Error: {error}. " "Please return ONLY the JSON object."
)

ANTHROPIC_SYSTEM_ONLY_TRIGGER = "Generate the content as specified."
TUTOR_DISPLAY_NAME = "Lingu"

_LANGUAGE_PROMPT_OVERLAYS: dict[str, str] = {
    "cs-CZ": """
Language-specific guidance:
- Use contemporary standard Czech as used in Czechia. Preserve Czech diacritics, including vowel length, ě and ř, and natural compound spelling. Distinguish standard, common spoken Czech and regional usage without treating every conversational variant as an error or substituting Slovak or Polish forms.
- Build from the alphabet, vowel length independent of first-syllable stress, palatal consonants and ř to gender, animacy, agreement and the seven cases. Introduce case endings with their communicative functions and verb or preposition government; do not import English articles.
- Teach imperfective and perfective aspect through context, distinguishing process, repetition and bounded result rather than equating aspect with tense. Develop motion verbs and prefixes gradually. Preserve natural past-tense agreement, conditional auxiliaries and reflexive se/si and svůj with explicit referents.
- Teach clitic placement by prosodic and syntactic units rather than a rigid second-written-word rule. Respect information structure, negative concord, numeral agreement and the scope of focus particles. Use ty or vy consistently with the relationship, and distinguish polite singular address from plural agreement.
- Progress from everyday interaction to interpretation, negotiation, mediation, humour and precise reformulation across registers. Preserve participants, source attribution, conditions, scope and degree of certainty. Give assessment questions enough context for exactly one accepted answer.
- Use varied everyday and cultural settings across Czechia, including Bohemia, Moravia and Czech Silesia, public transport, libraries, literature, music, regional life and contemporary debates. Avoid stereotypes and distinguish Czech from the separate Slovak language.
""".strip(),
    "da-DK": """
Language-specific guidance:
- Use contemporary standard Danish as used in Denmark. Preserve æ, ø and å as distinct letters, Danish compound spelling and capitalization. Recognize regional pronunciation and usage without substituting Swedish or Norwegian forms.
- Build from vowel quality and length, soft d, natural reductions and stød to en/et gender, plurals, definiteness and adjective agreement. Teach stød through listening and lexical examples; do not present it as obligatory in every stressed syllable or impose it on all dialects.
- Distinguish suffix definiteness from the article with an attributive adjective: huset, det store hus. Do not import Swedish double definiteness. Teach verb-second main clauses by constituents and contrast subordinate placement of ikke, with context for valid spoken alternatives.
- Teach har/er in perfect constructions, tense perspective, particle verbs and reflexive sin/sit/sine with explicit referents. Preserve the contrast between infinitive and present -r, and introduce Danish number words and time expressions through practical use rather than English word order.
- Use du as ordinary singular address and I as plural; explain De as a marked formal choice rather than default politeness. Progress from everyday requests and repair to negotiation, source attribution, humour and precise reformulation. Preserve participants, scope, conditions and degree of certainty; assessment questions require context for exactly one accepted answer.
- Use varied everyday and cultural settings in Denmark, including regional life, libraries, associations, transport, literature and design. Avoid stereotypes and distinguish Danish from the separate languages and perspectives of Greenland and the Faroe Islands when discussing the wider realm.
""".strip(),
    "sv-SE": """
Language-specific guidance:
- Use contemporary standard Swedish as used in Sweden. Preserve å, ä and ö as distinct letters, natural compound spelling and Swedish capitalization. Recognize regional Swedish and Finland-Swedish as valid varieties when comparing them, without replacing the selected Sweden usage.
- Build from vowel-consonant length contrasts, vowel quality and intelligible phrase stress to en/ett gender, plurals, definiteness, adjective agreement and possessives. Introduce pitch accents through listening without imposing one regional melody as universally correct.
- Teach verb-second main clauses by sentence constituents, not word counts; contrast subordinate-clause word order and the placement of inte. Distinguish supine after har/hade from agreeing participles, tense perspective, particle verbs and reflexive sin/sitt/sina with explicit referents. Do not calque English progressive forms or obligatory tense backshift.
- Use du as ordinary singular address; ni is plural and is not automatically a more polite singular choice. Distinguish de/dem in neutral edited writing while recognizing dom in speech and informal contexts. Teach requests, refusals, repair and mediation through realistic interaction.
- Progress from everyday tasks to nuanced interpretation, register, source attribution and negotiation. Preserve participants, negation scope, conditions, time and degree of commitment in reformulations. Do not mark valid contextual or regional alternatives as errors; placement questions require enough context for exactly one accepted answer.
- Use varied Swedish everyday and cultural settings, including regional diversity, public services, associations and nature. Avoid stereotypes or treating cultural tendencies as universal rules. Explain allemansrätten with responsibilities and local restrictions rather than unlimited access claims.
""".strip(),
    "ru-RU": """
Language-specific guidance:
- Use standard contemporary Russian as used in Russia, written in Cyrillic. Preserve ё where appropriate; do not replace Russian text with transliteration. Use stress marks selectively for pronunciation teaching, not as a substitute for ordinary spelling.
- Build from Cyrillic letters, lexical stress, vowel reduction and hard/soft consonants to gender, agreement, the six cases and verb government. Introduce case forms through communicative uses and level-appropriate examples rather than unexplained full paradigms.
- Teach imperfective/perfective aspect through context, including process, repetition, general fact and bounded result. Do not equate aspect mechanically with tense or imply that every imperfective past action was unfinished. Distinguish unidirectional and multidirectional motion verbs and the effects of prefixes.
- Use ты and вы consistently for the relationship and situation; explain names and patronymics without assuming that every formal exchange requires one. Respect natural Russian word order, information focus, negation and numeral agreement instead of calquing English.
- Progress towards contextual interpretation, register control, negotiation, mediation and precise reformulation. Preserve participants, scope, source attribution and degree of certainty; distinguish valid alternatives from errors. Assessment items need enough context for exactly one accepted answer.
- Use varied everyday and cultural contexts without assuming that all Russian speakers share one nationality, lifestyle or opinion. Explain colloquial, literary and regional usage when relevant instead of presenting it as universally interchangeable.
""".strip(),
    "nl-NL": """
Language-specific guidance:
- Use standard Dutch as used in the Netherlands, with natural vocabulary, spelling and pronunciation guidance.
- Teach nouns with de/het and their plurals; attend to adjective endings, vowel spelling, verb-second main clauses, subordinate verb groups, separable verbs, er, and niet/geen.
- Use je/jij or u consistently for the relationship and register. Both u hebt and u heeft are standard; recognize valid verb-cluster orders and regional standard variants rather than treating them as universal errors.
- Build from everyday interaction to nuanced interpretation and register control. Give assessment questions enough context for exactly one answer; preserve participants, scope, certainty and source attribution in reformulations.
- Prefer Netherlands contexts and usage such as fiets, pinpas, huisarts and gemeente. Label Belgian or Surinamese usage explicitly when comparing varieties; do not substitute German or English grammar or vocabulary.
""".strip(),
    "en-US": """
Language-specific guidance:
- Use American English spelling, vocabulary, punctuation, and idiom consistently.
- Prefer US forms such as color, center, organize, apartment, elevator, truck, and vacation.
- Avoid British-only spelling and vocabulary unless explicitly comparing variants.
""".strip(),
    "en-GB": """
Language-specific guidance:
- Use British English spelling, vocabulary, punctuation, and idiom consistently.
- Prefer UK forms such as colour, centre, organise, flat, lift, lorry, and holiday.
- Avoid American-only spelling and vocabulary unless explicitly comparing variants.
""".strip(),
    "es-ES": """
Language-specific guidance:
- Use Peninsular Spanish from Spain consistently.
- Prefer Spain usage, including vosotros for informal plural address when appropriate.
- Avoid voseo and Latin American-only vocabulary unless explicitly comparing variants.
- Pay close attention to accents, gender, number agreement, and natural Spain Spanish phrasing.
""".strip(),
    "it-IT": """
Language-specific guidance:
- Use standard Italian as used in Italy consistently.
- Pay close attention to articles, gender, number agreement, articulated prepositions, and clitic pronouns.
- Use tu or Lei consistently according to the context and learner level.
- Avoid strong regionalisms unless explicitly teaching or comparing them.
""".strip(),
    "pl-PL": """
Language-specific guidance:
- Use standard Polish as used in Poland consistently.
- Pay close attention to grammatical gender, case endings, verb aspect, and numeral agreement.
- Distinguish perfective and imperfective forms whenever the meaning depends on completion, repetition, or result.
- Avoid English word order and calques; use natural Polish phrasing and spelling with diacritics.
""".strip(),
    "pt-BR": """
Language-specific guidance:
- Use Brazilian Portuguese spelling, vocabulary, syntax, and register consistently.
- Prefer Brazilian forms such as celular, ônibus, café da manhã, trem, banheiro, and suco.
- Use estar + gerund for ongoing actions. Teach você/vocês with third-person agreement and a gente with singular agreement; explain regional tu usage without treating it as universally wrong.
- Prefer natural Brazilian pronoun placement; distinguish conversational proclisis from formal written conventions. Do not mark valid optional articles before possessives or personal names as errors.
- Use subjuntivo terminology and Brazilian cultural contexts. Avoid Portugal-only usage unless explicitly comparing varieties.
""".strip(),
    "pt-PT": """
Language-specific guidance:
- Use European Portuguese from Portugal consistently.
- Avoid Brazilian Portuguese vocabulary, syntax, and pronoun placement unless explicitly comparing variants.
- Prefer Portugal usage such as telemóvel, autocarro, pequeno-almoço, and comboio.
- Pay close attention to European Portuguese clitic placement, contractions, accents, and register.
""".strip(),
    "fr-FR": """
Language-specific guidance:
- Use standard French from France consistently.
- Pay close attention to accents, elision, contractions, gender, number agreement, and register.
- Use tu or vous consistently according to the context and learner level.
- Avoid Canadian or other regional French variants unless explicitly comparing them.
""".strip(),
    "de-DE": """
Language-specific guidance:
- Use standard German spelling and vocabulary as used in Germany consistently.
- Pay close attention to noun capitalization, grammatical gender, cases, adjective endings, and verb position.
- Use du or Sie consistently according to the context and learner level.
- Avoid Austrian or Swiss variants unless explicitly comparing them.
""".strip(),
    "ja-JP": """
Language-specific guidance:
- Use standard Japanese as used in Japan consistently.
- Use Japanese script naturally: hiragana, katakana, and level-appropriate kanji. Use romaji only as a short support aid for beginners or when explicitly teaching pronunciation.
- Pay close attention to particles, politeness level, verb forms, counters, and natural word order.
- Keep register consistent with the learner level; avoid abrupt shifts between plain and polite style unless teaching the contrast.
""".strip(),
    "ko-KR": """
Language-specific guidance:
- Use standard Korean as used in South Korea consistently.
- Use Hangul as the primary script. Use romanization only as a short support aid for beginners or when explicitly teaching pronunciation.
- Pay close attention to particles, speech level, honorifics, verb endings, batchim, and natural Korean phrasing.
- Avoid North Korean vocabulary, spelling, or usage unless explicitly comparing variants.
""".strip(),
    "zh-CN": """
Language-specific guidance:
- Use Mainland China Standard Mandarin (Putonghua) consistently.
- Use simplified Chinese characters. Use pinyin with tone marks only as support for pronunciation or beginner scaffolding, never as the main writing system.
- Pay close attention to tones, measure words, aspect particles, word order, and natural Mainland usage.
- Avoid Traditional Chinese, Cantonese, Taiwan, Hong Kong, or Macau variants unless explicitly comparing them.
""".strip(),
}

_LANGUAGE_PROMPT_OVERLAY_ALIASES: dict[str, str] = {
    "cs": "cs-CZ",
    "da": "da-DK",
    "sv": "sv-SE",
    "ru": "ru-RU",
    "nl": "nl-NL",
    "de": "de-DE",
    "fr": "fr-FR",
    "es": "es-ES",
    "it": "it-IT",
    "pl": "pl-PL",
    "pt": "pt-PT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
}


def get_language_prompt_overlay(target_language: str) -> str:
    """Return concise language/variant guidance for prompt composition."""
    canonical_language = _LANGUAGE_PROMPT_OVERLAY_ALIASES.get(target_language, target_language)
    return _LANGUAGE_PROMPT_OVERLAYS.get(canonical_language, "")


MEMORY_SYSTEM_INSTRUCTION_BASE = """
Memory capability: use the save_user_memory tool when you genuinely learn a new,
durable fact about the student that would help personalise future interactions,
such as personal details, preferences, tastes, hobbies, profession, plans, goals,
learning style, or motivations. Most replies should not call the tool. Never save
temporary details, uncertain inferences, conversation summaries, or instructions.
Never save fictional identities, preferences, plans or experiences from roleplay,
hypothetical scenarios or practice examples as facts about the student. Treat statements
made in character as fictional unless the student separately confirms they are real,
durable facts about themselves outside the scenario. When unsure, skip saving.
Do not save facts already present in the supplied memories. Write each memory as
a concise, self-contained fact in the student's native language ({native_language_name})
so the student can review it in Settings. Continue the visible response after the tool result and never
claim the memory was saved when the tool reports an error.
"""


def get_memory_system_instruction(native_language_name: str) -> str:
    """Return the shared native memory-tool policy."""
    return MEMORY_SYSTEM_INSTRUCTION_BASE.format(native_language_name=native_language_name)
