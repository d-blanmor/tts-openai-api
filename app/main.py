from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse

from app.config import settings
from app.providers.registry import get_provider
from app.schemas import ModelInfo, ModelsResponse, TTSRequest
from app.services.tts_service import TTSService

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

MODEL_LIST = [
    ModelInfo(id=settings.DEFAULT_PROVIDER),
]


def resolve_model_id(model: str | None) -> str:
    candidate = (model or settings.DEFAULT_PROVIDER).strip()
    if not candidate:
        return settings.DEFAULT_PROVIDER

    normalized = candidate.lower()

    try:
        get_provider(candidate)
    except ValueError:
        return settings.DEFAULT_PROVIDER

    if normalized.startswith("tts-bridge/"):
        return candidate

    if normalized in {"voicebox", "azure", "google", "elevenlabs"}:
        return f"tts-bridge/{normalized}"

    return settings.DEFAULT_PROVIDER


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/v1/models")
async def list_models() -> ModelsResponse:
    return ModelsResponse(data=MODEL_LIST)


@app.get("/v1/models/{model}")
async def get_model(model: str) -> ModelInfo:
    return ModelInfo(id=resolve_model_id(model))


@app.get("/v1/audio/voices")
async def list_voices() -> dict:
    provider = get_provider(settings.DEFAULT_PROVIDER)
    if provider.name != "voicebox":
        return {"voices": [], "default_voice": None}

    profiles = await provider.list_voices()  # type: ignore[attr-defined-method]
    default_voice = settings.VOICEBOX_DEFAULT_PROFILE_ID or (profiles[0]["id"] if profiles else None)

    voices = []
    for profile in profiles:
        voice_id = profile.get("id")
        voice = {
            "id": voice_id,
            "name": profile.get("name"),
            "target_quality": profile.get("default_engine") or profile.get("voice_type") or "default",
            "training_duration": profile.get("generation_count", 0),
            "overall_grade": profile.get("sample_count", 0),
        }
        voices.append(voice)

    return {"voices": voices, "default_voice": default_voice}


@app.get("/v1/download/{filename}")
async def generate_download(filename: str) -> dict[str, str]:
    return {"filename": filename, "status": "not_implemented"}


@app.post("/v1/audio/speech")
async def generate_speech(
    request: TTSRequest,
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    if settings.REQUIRE_AUTH and authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    service = TTSService()
    audio_bytes = await service.generate(request)

    content_type = {
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "opus": "audio/ogg",
        "aac": "audio/aac",
    }.get(request.response_format, "audio/mpeg")

    return StreamingResponse(iter([audio_bytes]), media_type=content_type)


@app.post("/v1/audio/voices/combine")
async def combine(
    request: TTSRequest,
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    if settings.REQUIRE_AUTH and authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    return {"status": "not_implemented"}
