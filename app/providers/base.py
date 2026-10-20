from abc import ABC, abstractmethod


class BaseTTSProvider(ABC):
    """Common interface for all TTS backends."""

    name: str = "base"
    default_voice: str | None = None

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: str | None,
        response_format: str,
        speed: float,
    ) -> bytes:
        """Return synthesized audio bytes for the requested text."""
