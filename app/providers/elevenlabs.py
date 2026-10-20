from app.providers.base import BaseTTSProvider


class ElevenLabsProvider(BaseTTSProvider):
    name = "elevenlabs"
    default_voice = "bella"

    async def synthesize(
        self,
        text: str,
        voice: str | None,
        response_format: str,
        speed: float,
    ) -> bytes:
        # TODO: Replace this placeholder with a real ElevenLabs API integration.
        # Keeping it here guarantees the scaffold compiles and can be extended.
        return b""
