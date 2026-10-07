import pytest

from app.services.chat_markdown import chat_markdown_to_speech


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Use **went**, not *goed*.", "Use went, not goed."),
        ("Try ***this*** and __that__.", "Try this and that."),
        ("Hello.\n\nHow are you?", "Hello.\n\nHow are you?"),
        ("First line\nsecond line.  \nThird line.", "First line\nsecond line.\nThird line."),
        ("- I went home.\n- She went shopping.", "I went home.\nShe went shopping."),
        ("3. **Go** home\n4. *Stay* here", "Go home.\nStay here."),
        (
            "Examples:\n\n- Hello!\n- Goodbye\n\nYour turn.",
            "Examples:\n\nHello!\nGoodbye.\n\nYour turn.",
        ),
        ("- Animals:\n  - cats\n  - dogs\n- Birds", "Animals:\ncats.\ndogs.\nBirds."),
        ('- Say "Hello!"\n- Say "Goodbye"', 'Say "Hello!"\nSay "Goodbye".'),
        (
            "2026, 3.14, -5 and 2 * 3; well-known, user_name.",
            "2026, 3.14, -5 and 2 * 3; well-known, user_name.",
        ),
        (r"Literal \*word\* and \_term\_.", "Literal *word* and _term_."),
        ("An unfinished **correction", "An unfinished **correction"),
        ("# Example\n\n> Read [this](https://example.com).", "Example\n\nRead this."),
        ("`went`\n\n```text\nI went home.\n```", "went\n\nI went home."),
        (
            "A <b>word</b> and ![description](https://example.com/image.png).",
            "A word and description.",
        ),
        ("<script>alert('hidden')</script>\n\nHello.", "Hello."),
        ("---", ""),
    ],
)
def test_chat_speech_preserves_content_and_spoken_boundaries(text, expected):
    assert chat_markdown_to_speech(text) == expected


@pytest.mark.parametrize("language", ["ja-JP", "zh-CN"])
def test_cjk_list_boundaries_use_full_width_stops(language):
    assert chat_markdown_to_speech("- **你好**\n- 再见！", language) == "你好。\n再见！"


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("caf&#233;", "café"),
        ("&#50; cats", "2 cats"),
        ("caf&#xE9; &amp; tea", "café & tea"),
        (r"\*cats\* and \_dogs\_", "*cats* and _dogs_"),
        ("**caf&#233;**", "café"),
        ("first\\\nsecond", "first\nsecond"),
        ("first  \nsecond", "first\nsecond"),
        ("first\nsecond", "first\nsecond"),
        ("a <b>word</b>", "a word"),
        ("`<b>word</b>`", "<b>word</b>"),
        (r"a \<b>word\</b>", "a <b>word</b>"),
        ("outer ![first\\\nsecond](https://example.com/nested.png)", "outer first\nsecond"),
    ],
)
@pytest.mark.parametrize("reference", [False, True])
def test_image_descriptions_preserve_readable_content(label, expected, reference):
    text = (
        f"![{label}][ref]\n\n[ref]: https://example.com/image.png"
        if reference
        else f"![{label}](https://example.com/image.png)"
    )
    assert chat_markdown_to_speech(text) == expected


@pytest.mark.parametrize(
    "destination",
    [
        "https://example.com",
        "javascript:alert%281%29",
        "file:///private/example",
        "data:text/plain,hello",
    ],
)
@pytest.mark.parametrize(
    "text",
    [
        "Read [**this**]({destination}).",
        "Read [**this**][ref].\n\n[ref]: {destination}",
        "Read ![**this**]({destination}).",
    ],
)
def test_only_link_labels_and_image_descriptions_are_spoken_for_every_protocol(text, destination):
    assert chat_markdown_to_speech(text.format(destination=destination)) == "Read this."


@pytest.mark.parametrize(
    "label",
    [
        "https://example.com/%32%30%32%36",
        "https://xn--caf-dma.example/%C3%A9",
        "file:///example/%32%30%32%36",
        "hello@xn--caf-dma.example",
    ],
)
def test_autolink_labels_remain_verbatim(label):
    assert chat_markdown_to_speech(f"Read <{label}>.") == f"Read {label}."
