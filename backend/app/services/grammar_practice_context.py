"""Bounded, lossless reference data for grammar generation and voice practice."""

import json
from html import escape

MAX_VOICE_CONTEXT_CHARS = 65_536
# A quoted character occupies seven characters after JSON and HTML escaping.
# Reserve for five 500-character answers plus timestamps and result metadata.
ANSWER_CONTEXT_RESERVE = 20_480


def serialize_grammar_context(topic_snapshot: dict, challenges: list, answers: list) -> str:
    context = escape(
        json.dumps(
            {
                "title": topic_snapshot.get("title", ""),
                "lesson_type": "grammar",
                "topic": topic_snapshot,
                "exercises": challenges,
                "answered_exercises": answers,
            },
            ensure_ascii=False,
        )
    )
    if len(context) > MAX_VOICE_CONTEXT_CHARS:
        raise ValueError("Grammar practice context exceeds the voice budget")
    return context
