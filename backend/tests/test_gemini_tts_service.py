import asyncio
import base64
import io
import json
import logging
import wave
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest

from app.services import gemini_tts_service as gemini
from app.services.gemini_tts_service import GEMINI_VOICES, GeminiTTSService


def make_wav(channels=1, sample_width=2, sample_rate=24000, frames=b"\x00\x00" * 24):
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)
    return buffer.getvalue()


def make_response(audio=None):
    return {
        "status": "completed",
        "steps": [
            {
                "type": "model_output",
                "content": [
                    {
                        "type": "audio",
                        "mime_type": "audio/wav",
                        "data": base64.b64encode(make_wav() if audio is None else audio).decode(),
                    }
                ],
            }
        ],
    }


@pytest.fixture
def service():
    return GeminiTTSService(api_key="test-key")


@pytest.fixture
def mock_http(monkeypatch):
    client_class = httpx.AsyncClient

    def install(handler):
        client = client_class(transport=httpx.MockTransport(handler))
        monkeypatch.setattr(gemini.httpx, "AsyncClient", lambda: client)
        return client

    return install


@pytest.mark.parametrize("voice,resolved_voice", [("female", "Kore"), ("male", "Puck")])
async def test_request_contract_returns_original_wav(service, mock_http, voice, resolved_voice):
    text = "  Read **exactly** this.\nDo not translate.  "

    def handler(request):
        assert request.method == "POST"
        assert str(request.url) == "https://generativelanguage.googleapis.com/v1beta/interactions"
        assert request.headers["x-goog-api-key"] == "test-key"
        assert request.extensions["timeout"]["read"] == 50.0
        assert json.loads(request.content) == {
            "model": "gemini-3.8-flash-tts",
            "input": [
                {
                    "type": "user_input",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                            "annotations": [
                                {
                                    "type": "speech_metadata",
                                    "style": "Warm, clear delivery with natural pronunciation.",
                                }
                            ],
                        }
                    ],
                }
            ],
            "response_format": {"type": "audio", "mime_type": "audio/wav", "sample_rate": 24000},
            "generation_config": {
                "speech_config": [{"voice": resolved_voice, "language": "en-US"}]
            },
            "store": False,
            "stream": False,
        }
        return httpx.Response(200, json=make_response())

    client = mock_http(handler)
    assert await service.synthesize(text, voice, "en-US") == make_wav()
    assert service.audio_extension == "wav"
    assert service.media_type == "audio/wav"
    assert client.is_closed


@pytest.mark.parametrize(
    "language,expected",
    [
        (None, None),
        ("en", "en-GB"),
        ("en-GB", "en-GB"),
        ("en-US", "en-US"),
        ("es", "es-ES"),
        ("pt", "pt-PT"),
        ("pt-PT", "pt-PT"),
        ("pt-BR", "pt-BR"),
        ("fr", "fr-FR"),
        ("de", "de-DE"),
        ("it", "it-IT"),
        ("ja", "ja-JP"),
        ("ko", "ko-KR"),
        ("zh", "zh-CN"),
        ("pl", "pl-PL"),
        ("nl", "nl-NL"),
        ("ro", "ro-RO"),
        ("ru", "ru-RU"),
        ("tr", "tr-TR"),
        ("sv", "sv-SE"),
        ("da", "da-DK"),
        ("da-DK", "da-DK"),
        ("cs", "cs-CZ"),
        ("cs-CZ", "cs-CZ"),
        ("fi", "fi-FI"),
        ("fi-FI", "fi-FI"),
        ("hr", "hr-HR"),
        ("hr-HR", "hr-HR"),
        ("fr-CA", "fr-CA"),
        ("zh-TW", "zh-TW"),
    ],
)
async def test_language_context_preserves_regions(service, mock_http, language, expected):
    def handler(request):
        config = json.loads(request.content)["generation_config"]["speech_config"][0]
        assert config == (
            {"voice": "Kore", "language": expected} if expected else {"voice": "Kore"}
        )
        return httpx.Response(200, json=make_response())

    mock_http(handler)
    await service.synthesize("Text", language=language)


@pytest.mark.parametrize("voice", ["nova", "Kore", "", "Female"])
async def test_invalid_voice_rejected_before_http(service, monkeypatch, voice):
    client = Mock()
    monkeypatch.setattr(gemini.httpx, "AsyncClient", client)
    with pytest.raises(ValueError, match="voice"):
        await service.synthesize("Text", voice)
    with pytest.raises(ValueError, match="voice"):
        service.get_cache_key("Text", voice)
    with pytest.raises(ValueError, match="voice"):
        GeminiTTSService("test-key", voice=voice)
    client.assert_not_called()


@pytest.mark.parametrize(
    "config",
    [
        {"api_key": " "},
        {"api_key": None},
        {"model": ""},
        {"female_voice": ""},
        {"male_voice": " "},
        {"voice": None},
        {"timeout": 0},
        {"timeout": -1},
        {"timeout": float("inf")},
        {"timeout": float("nan")},
        {"timeout": None},
        {"timeout": True},
    ],
)
def test_required_configuration_is_validated(config):
    with pytest.raises(ValueError):
        GeminiTTSService(**{"api_key": "test-key", **config})


@pytest.mark.parametrize("voice,expected", [(None, "Charon"), ("female", "Aoede")])
async def test_configurable_default_and_provider_voice_ids(mock_http, voice, expected):
    service = GeminiTTSService("test-key", voice="male", female_voice="Aoede", male_voice="Charon")

    def handler(request):
        config = json.loads(request.content)["generation_config"]["speech_config"]
        assert config == [{"voice": expected}]
        return httpx.Response(200, json=make_response())

    mock_http(handler)
    await service.synthesize("Text", voice)
    assert GEMINI_VOICES == frozenset({"female", "male"})


def test_cache_tracks_effective_configuration_and_language(service, monkeypatch):
    key = service.get_cache_key("Text", language="en-GB")
    assert key == service.get_cache_key("Text", "female", "en")
    assert key != service.get_cache_key("Text", "male", "en-GB")
    assert key != service.get_cache_key("Text", language="en-US")
    assert key != service.get_cache_key("Text")
    assert key != service.get_cache_key("Other text", language="en-GB")
    assert service.get_cache_key("Text", language="pt-PT") != service.get_cache_key(
        "Text", language="pt-BR"
    )
    for attribute, value in [
        ("model", "other-model"),
        ("female_voice", "Aoede"),
        ("audio_extension", "mp3"),
        ("media_type", "audio/mpeg"),
    ]:
        with monkeypatch.context() as context:
            context.setattr(service, attribute, value)
            assert key != service.get_cache_key("Text", language="en-GB")
    monkeypatch.setattr(gemini, "_SPEECH_STYLE", "Updated style")
    assert key != service.get_cache_key("Text", language="en-GB")


def test_cache_uses_real_voice_not_display_label(service):
    service.male_voice = service.female_voice
    assert service.get_cache_key("Text", "female") == service.get_cache_key("Text", "male")


@pytest.mark.parametrize("text", ["", " \n\t "])
async def test_empty_text_skips_http(service, monkeypatch, text):
    client = Mock()
    monkeypatch.setattr(gemini.httpx, "AsyncClient", client)
    assert await service.synthesize(text) == b""
    client.assert_not_called()


async def test_explicit_empty_language_is_rejected(service):
    with pytest.raises(ValueError, match="language"):
        await service.synthesize("Text", language=" ")
    with pytest.raises(ValueError, match="language"):
        service.get_cache_key("Text", language=" ")


@pytest.mark.parametrize("status", [400, 401, 429, 500])
async def test_http_errors_are_not_retried_or_logged(service, mock_http, caplog, status):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, json={"error": "sensitive-provider-body"})

    client = mock_http(handler)
    with caplog.at_level(logging.INFO):
        with pytest.raises(httpx.HTTPStatusError):
            await service.synthesize("sensitive-transcript")
    assert len(calls) == 1
    assert client.is_closed
    assert "sensitive-provider-body" not in caplog.text
    assert "sensitive-transcript" not in caplog.text
    assert "test-key" not in caplog.text


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"status": "completed"},
        {"status": "completed", "steps": []},
        {"status": "completed", "steps": [None]},
        {"status": "completed", "steps": [{"type": "model_output", "content": None}]},
        {"status": "completed", "steps": [{"type": "model_output", "content": [None]}]},
    ],
)
async def test_malformed_response_rejected(service, mock_http, payload):
    mock_http(lambda request: httpx.Response(200, content=json.dumps(payload)))
    with pytest.raises(RuntimeError):
        await service.synthesize("Text")


@pytest.mark.parametrize("status", ["in_progress", "failed", "cancelled", None])
async def test_incomplete_status_rejected_even_with_valid_audio(service, mock_http, status):
    payload = make_response()
    payload["status"] = status
    mock_http(lambda request: httpx.Response(200, json=payload))
    with pytest.raises(RuntimeError, match="did not complete"):
        await service.synthesize("Text")


@pytest.mark.parametrize(
    "part",
    [
        {"type": "audio", "mime_type": "audio/mp3", "data": "YWJj"},
        {"type": "audio", "mime_type": "audio/wav", "data": ""},
        {"type": "audio", "mime_type": "audio/wav", "data": 123},
        {"type": "audio", "mime_type": "audio/wav", "data": "%%%"},
        {"type": "audio", "mime_type": "audio/wav", "data": "YQ"},
        {"type": "audio", "mime_type": "audio/wav", "data": "é"},
        {"type": "audio", "mime_type": "audio/wav", "uri": "https://example.com/audio.wav"},
    ],
)
async def test_invalid_audio_parts_are_not_returned_or_fetched(service, mock_http, part):
    payload = make_response()
    payload["steps"][0]["content"] = [part]
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json=payload)

    mock_http(handler)
    with pytest.raises(RuntimeError):
        await service.synthesize("Text")
    assert len(requests) == 1


@pytest.mark.parametrize(
    "audio",
    [
        b"",
        b"not a WAV",
        make_wav(frames=b""),
        make_wav(channels=2),
        make_wav(sample_width=1),
        make_wav(sample_width=3),
        make_wav(sample_rate=48000),
        make_wav()[:-1],
        make_wav(frames=b"\x00" * 47),
    ],
)
async def test_invalid_or_truncated_wav_rejected(service, mock_http, audio):
    mock_http(lambda request: httpx.Response(200, json=make_response(audio)))
    with pytest.raises(RuntimeError):
        await service.synthesize("Text")


def test_truncated_frames_rejected_even_with_corrected_riff_size():
    audio = bytearray(make_wav()[:-2])
    audio[4:8] = (len(audio) - 8).to_bytes(4, "little")
    with pytest.raises(RuntimeError, match="truncated"):
        GeminiTTSService._extract_wav(make_response(bytes(audio)))


def test_compressed_wav_is_rejected():
    audio = bytearray(make_wav())
    audio[20:22] = (7).to_bytes(2, "little")
    with pytest.raises(RuntimeError, match="PCM16"):
        GeminiTTSService._extract_wav(make_response(bytes(audio)))


@pytest.mark.parametrize(
    "offset,value,width",
    [(34, 15, 2), (32, 4, 2), (28, 96000, 4)],
)
def test_inconsistent_pcm_header_is_rejected(offset, value, width):
    audio = bytearray(make_wav())
    audio[offset : offset + width] = value.to_bytes(width, "little")
    with pytest.raises(RuntimeError, match="PCM16"):
        GeminiTTSService._extract_wav(make_response(bytes(audio)))


def test_truncated_trailing_chunk_is_rejected():
    audio = bytearray(make_wav() + b"JUNK" + (4).to_bytes(4, "little") + b"ab")
    audio[4:8] = (len(audio) - 8).to_bytes(4, "little")
    with pytest.raises(RuntimeError, match="truncated"):
        GeminiTTSService._extract_wav(make_response(bytes(audio)))


def test_complete_metadata_chunk_is_preserved():
    audio = bytearray(make_wav() + b"JUNK" + (4).to_bytes(4, "little") + b"abcd")
    audio[4:8] = (len(audio) - 8).to_bytes(4, "little")
    assert GeminiTTSService._extract_wav(make_response(bytes(audio))) == bytes(audio)


def test_multiple_audio_parts_are_not_silently_discarded():
    payload = make_response()
    payload["steps"].append(payload["steps"][0])
    with pytest.raises(RuntimeError, match="exactly one"):
        GeminiTTSService._extract_wav(payload)


def test_only_model_output_audio_is_used():
    payload = make_response()
    payload["steps"].insert(0, {"type": "user_input", "content": [{"type": "audio"}]})
    payload["steps"][1]["content"].insert(0, {"type": "text", "text": "Metadata"})
    assert GeminiTTSService._extract_wav(payload) == make_wav()


async def test_non_json_response_rejected(service, mock_http):
    mock_http(lambda request: httpx.Response(200, content=b"not JSON"))
    with pytest.raises(RuntimeError, match="JSON"):
        await service.synthesize("Text")


async def test_success_logs_only_metadata(service, mock_http, caplog):
    mock_http(lambda request: httpx.Response(200, json=make_response()))
    with caplog.at_level(logging.INFO):
        await service.synthesize("sensitive-transcript")
    assert "request_ok" in caplog.text
    assert "sensitive-transcript" not in caplog.text
    assert "test-key" not in caplog.text
    assert make_response()["steps"][0]["content"][0]["data"] not in caplog.text


async def test_health_only_lists_models(service, mock_http):
    def handler(request):
        assert request.method == "GET"
        assert str(request.url) == "https://generativelanguage.googleapis.com/v1beta/models"
        assert request.headers["x-goog-api-key"] == "test-key"
        assert request.extensions["timeout"]["read"] == 5.0
        return httpx.Response(200, json={"models": []})

    client = mock_http(handler)
    await service.health()
    assert client.is_closed


async def test_health_authentication_failure_propagates(service, mock_http):
    mock_http(lambda request: httpx.Response(401))
    with pytest.raises(httpx.HTTPStatusError):
        await service.health()


async def test_http_timeout_is_propagated_without_retry(service, mock_http):
    calls = []

    def handler(request):
        calls.append(request)
        raise httpx.ReadTimeout("timeout", request=request)

    client = mock_http(handler)
    with pytest.raises(httpx.ReadTimeout):
        await service.synthesize("Text")
    assert len(calls) == 1
    assert client.is_closed


@pytest.mark.parametrize("operation", ["synthesize", "health"])
async def test_total_deadline_cancels_http_and_closes_client(service, mock_http, operation):
    service.timeout = 0.01
    cancelled = asyncio.Event()

    async def handler(request):
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    client = mock_http(handler)
    with pytest.raises(TimeoutError):
        if operation == "synthesize":
            await service.synthesize("Text")
        else:
            await service.health()
    assert cancelled.is_set()
    assert client.is_closed


async def test_total_deadline_includes_synchronous_validation(service, mock_http, monkeypatch):
    mock_http(lambda request: httpx.Response(200, json=make_response()))
    clock = Mock(side_effect=[0.0, service.timeout + 1.0])
    monkeypatch.setattr(gemini, "time", SimpleNamespace(perf_counter=clock))
    with pytest.raises(TimeoutError, match="deadline"):
        await service.synthesize("Text")


async def test_caller_cancellation_closes_http_client(service, mock_http):
    started = asyncio.Event()

    async def handler(request):
        started.set()
        await asyncio.Event().wait()

    client = mock_http(handler)
    task = asyncio.create_task(service.synthesize("Text"))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert client.is_closed
