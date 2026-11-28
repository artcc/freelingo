import asyncio
import base64
import io
import wave
from functools import partial
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi import FastAPI, WebSocket
from httpx_ws import aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport

from app.core.config import settings
from app.main import app
from app.routers import tts as tts_router
from app.services import openai_realtime_tts
from app.services.tts_service import OpenAITTSService

MODEL = "gpt-realtime-2.1-mini"


def delta(samples):
    return {
        "type": "response.output_audio.delta",
        "response_id": "resp_test",
        "delta": base64.b64encode(samples).decode(),
    }


def done(status="completed"):
    return {"type": "response.done", "response": {"id": "resp_test", "status": status}}


async def test_realtime_synthesizes_one_complete_wav_over_websocket(monkeypatch):
    provider = FastAPI()
    requests = []
    monkeypatch.setenv("OPENAI_BASE_URL", "https://regional.example.test/a%2Fb/v1?region=eu")
    monkeypatch.setenv("OPENAI_PROJECT_ID", "test-project")
    # One event exceeds the transport's default 64 KiB limit after base64 encoding.
    samples = bytes(range(256)) * 216

    @provider.websocket("/a/b/v1/realtime")
    async def speech(ws: WebSocket):
        await ws.accept()
        destination = (ws.url.hostname, ws.headers["authorization"], ws.headers["openai-project"])
        requests.append(destination)
        requests.append((ws.scope["raw_path"].split(b"?")[0], ws.query_params["region"]))
        requests.append(ws.query_params["model"])
        await ws.send_json({"type": "session.created"})
        requests.append(await ws.receive_json())
        await ws.send_json({"type": "session.updated"})
        requests.append(await ws.receive_json())
        await ws.send_json(delta(samples))
        await ws.send_json(delta(b"\x01\x00"))
        await ws.send_json(done())
        await ws.receive()

    text = "Do you speak English?"
    service = OpenAITTSService("test-key", MODEL, "female", speed=0.9)
    async with httpx.AsyncClient(transport=ASGIWebSocketTransport(app=provider)) as client:
        monkeypatch.setattr(openai_realtime_tts, "aconnect_ws", partial(aconnect_ws, client=client))
        audio = await service.synthesize(text, "male", "en-GB")

    destination, route, model, update, create = requests
    assert destination == ("regional.example.test", "Bearer test-key", "test-project")
    assert route == (b"/a%2Fb/v1/realtime", "eu")
    assert model == MODEL
    assert update["type"] == "session.update"
    session = update["session"]
    assert "British English" in session["instructions"]
    assert text not in session["instructions"]
    assert session["audio"]["output"] == {
        "format": {"type": "audio/pcm", "rate": 24000},
        "voice": "cedar",
        "speed": 0.9,
    }
    assert create["type"] == "response.create"
    assert create["response"]["conversation"] == "none"
    assert create["response"]["input"] == [
        {"type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}
    ]
    with wave.open(io.BytesIO(audio), "rb") as wav:
        assert (wav.getframerate(), wav.getsampwidth(), wav.getnchannels()) == (24000, 2, 1)
        assert wav.readframes(wav.getnframes()) == samples + b"\x01\x00"


@pytest.fixture
def mock_connection(monkeypatch):
    connection = MagicMock()
    socket = AsyncMock()
    socket.response = None
    connection.__aenter__.return_value = socket
    monkeypatch.setattr(openai_realtime_tts, "aconnect_ws", lambda *args, **kwargs: connection)
    return connection, socket


@pytest.mark.parametrize(
    "end",
    [
        done("incomplete"),
        {"type": "error"},
        {"type": "response.done", "response": {"status": "completed", "id": "other"}},
        {**delta(b""), "delta": "bad!"},
    ],
)
async def test_failed_realtime_preview_does_not_publish_partial_audio(
    end, client, test_user, monkeypatch, tmp_path, mock_connection
):
    _, headers = test_user
    connection, socket = mock_connection
    service = OpenAITTSService("test-key", MODEL, "female")
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(tts_router, "_PREVIEW_DIR", str(tmp_path))
    socket.receive_json.side_effect = [{"type": "session.updated"}, delta(b"ab"), end]
    with pytest.raises(RuntimeError, match="OpenAI Realtime TTS"):
        await client.get("/api/tts/preview/female", headers=headers)
    connection.__aexit__.assert_awaited_once()
    assert not list(tmp_path.iterdir())

    socket.receive_json.side_effect = [{"type": "session.updated"}, delta(b"cd"), done()]
    response = await client.get("/api/tts/preview/female", headers=headers)
    cached = await client.get("/api/tts/preview/female", headers=headers)
    assert response.status_code == cached.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content == cached.content
    assert [path.read_bytes() for path in tmp_path.glob("female-*.wav")] == [response.content]
    assert connection.__aenter__.await_count == 2


async def test_realtime_aborts_transport_when_graceful_close_stalls(monkeypatch):
    stream = AsyncMock()

    async def blocked_write(_data):
        await asyncio.Future()

    stream.write.side_effect = blocked_write
    socket = openai_realtime_tts._SpeechSocket(stream)
    monkeypatch.setattr(openai_realtime_tts, "_CLOSE_TIMEOUT", 0.01)
    await asyncio.wait_for(socket.close(), timeout=1)
    stream.write.assert_awaited_once()
    stream.aclose.assert_awaited_once()


@pytest.mark.parametrize("cancel", [True, False])
async def test_realtime_closes_when_interrupted_after_first_delta(mock_connection, cancel):
    connection, socket = mock_connection
    received = asyncio.Event()
    events = iter([{"type": "session.updated"}, delta(b"ab")])

    async def receive():
        if event := next(events, None):
            return event
        received.set()
        await asyncio.Future()

    socket.receive_json.side_effect = receive
    service = OpenAITTSService("test-key", MODEL, "female", timeout=1 if cancel else 0.03)
    task = asyncio.create_task(service.synthesize("Hola."))
    await asyncio.wait_for(received.wait(), timeout=1)
    if cancel:
        task.cancel()
    with pytest.raises(asyncio.CancelledError if cancel else TimeoutError):
        await task
    connection.__aexit__.assert_awaited_once()
