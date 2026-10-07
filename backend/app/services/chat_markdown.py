"""Convert written-chat Markdown to spoken text without changing stored messages."""

from markdown_it import MarkdownIt
from markdown_it.token import Token


class _SpeechMarkdownParser(MarkdownIt):
    def validateLink(self, url: str) -> bool:
        # This parser is only used for text extraction, never HTML rendering or fetching.
        # Recognize every destination like the frontend, then discard it, keeping its label.
        return True

    def normalizeLinkText(self, url: str) -> str:
        # Autolink labels are visible verbatim in chat, including percent escapes and punycode.
        return url


# Match the chat renderer's CommonMark syntax; HTML is parsed only to omit it.
_PARSER = _SpeechMarkdownParser("commonmark")
_SENTENCE_ENDINGS = ".!?;:…。！？；："
_CLOSING_MARKS = "\"'”’»」』)]}）】"


def _inline_text(tokens: list[Token]) -> str:
    parts: list[str] = []
    for token in tokens:
        if token.type in {"text", "text_special", "code_inline"}:
            parts.append(token.content)
        elif token.type in {"softbreak", "hardbreak"}:
            parts.append("\n")
        elif token.type == "image":
            parts.append(_inline_text(token.children or []))
    return "".join(parts)


def chat_markdown_to_speech(text: str, language: str | None = None) -> str:
    """Keep wording, plain punctuation and block boundaries; omit presentation markers."""
    parts: list[str] = []
    list_depth = 0
    previous_was_list = False
    full_stop = "。" if (language or "").split("-")[0] in {"ja", "zh"} else "."

    for token in _PARSER.parse(text):
        if token.type == "list_item_open":
            list_depth += 1
        elif token.type == "list_item_close":
            list_depth -= 1
        elif token.type in {"inline", "fence", "code_block"}:
            content = (
                _inline_text(token.children or []) if token.type == "inline" else token.content
            ).strip()
            if not content:
                continue
            in_list = list_depth > 0
            # A bare list item still needs a spoken boundary after its marker is removed.
            ending = content.rstrip(_CLOSING_MARKS)
            if in_list and ending and ending[-1] not in _SENTENCE_ENDINGS:
                content += full_stop
            if parts:
                parts.append("\n" if in_list and previous_was_list else "\n\n")
            parts.append(content)
            previous_was_list = in_list

    return "".join(parts)
