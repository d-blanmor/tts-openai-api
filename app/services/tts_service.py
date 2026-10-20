from fastapi import HTTPException

from app.providers.registry import get_provider
from app.schemas import TTSRequest


class TTSService:
    async def generate(self, request: TTSRequest) -> bytes:
        try:
            provider = get_provider(request.model)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        voice = request.voice or provider.default_voice
        return await provider.synthesize(
            text=request.input,
            voice=voice,
            response_format=request.response_format,
            speed=request.speed,
        )
