from app.providers.base import BaseTTSProvider


class AzureTTSProvider(BaseTTSProvider):
    name = "azure"
    default_voice = "en-US-JennyNeural"

    async def synthesize(
        self,
        text: str,
        voice: str | None,
        response_format: str,
        speed: float,
    ) -> bytes:
        # TODO: Replace this placeholder with a real Azure Speech integration.
        return b""
