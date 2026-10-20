# TTS OpenAI Bridge

This project provides a small Python FastAPI service that exposes an OpenAI-compatible TTS API and routes requests to external text-to-speech providers.

## Features

- OpenAI-like `/v1/audio/speech` endpoint
- Provider registry and adapter pattern
- Model aliases for multiple backends
- Configurable environment variables
- Simple scaffold ready for real backend integrations
- VoiceBox provider support for local voicebox-style TTS servers

## Quick start

1. Create a virtual environment
2. Install dependencies
3. Copy `.env.example` to `.env` and customize the keys
4. Run the app with Uvicorn

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes

- The provider classes in `app/providers` are intentionally scaffolded placeholders.
- The real API integrations will be added in subsequent iterations.
- Open WebUI can point to this service using an OpenAI-compatible base URL.

## Example request

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-bridge/voicebox",
    "input": "Hello from the VoiceBox bridge",
    "voice": "Isabella",
    "response_format": "wav",
    "speed": 1.0
  }'
```

## VoiceBox configuration

Set the following environment variables before running the app:

```env
VOICEBOX_BASE_URL=http://127.0.0.1:17493
VOICEBOX_API_KEY=
VOICEBOX_DEFAULT_PROFILE_ID=
REQUIRE_AUTH=false
```

The VoiceBox provider resolves the `voice` value against the list of existing profiles on the server. If a profile ID is configured in `VOICEBOX_DEFAULT_PROFILE_ID`, it is used as the fallback profile.
