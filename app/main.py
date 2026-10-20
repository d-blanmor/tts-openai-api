from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse

from app.config import settings
from app.schemas import ModelInfo, ModelsResponse, TTSRequest
from app.services.tts_service import TTSService

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

MODEL_LIST = [
    ModelInfo(id="tts-bridge/elevenlabs"),
    ModelInfo(id="tts-bridge/google"),
    ModelInfo(id="tts-bridge/azure"),
    ModelInfo(id="tts-bridge/voicebox"),
]


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/v1/models")
async def list_models() -> ModelsResponse:
    return ModelsResponse(data=MODEL_LIST)


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
