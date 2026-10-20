from app.providers.base import BaseTTSProvider


class GoogleTTSProvider(BaseTTSProvider):
    name = "google"
    default_voice = "en-US-Neural2-A"

    async def synthesize(
        self,
        text: str,
        voice: str | None,
        response_format: str,
        speed: float,
    ) -> bytes:
        # TODO: Replace this placeholder with actual Google Cloud TTS logic.
        return b""
