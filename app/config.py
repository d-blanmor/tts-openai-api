import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = os.getenv("APP_NAME", "tts-openai-bridge")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    REQUIRE_AUTH: bool = os.getenv("REQUIRE_AUTH", "false").lower() == "true"

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE_URL: str = os.getenv("OPENAI_API_BASE_URL", "/v1")

    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    GOOGLE_TTS_API_KEY: Optional[str] = os.getenv("GOOGLE_TTS_API_KEY")
    AZURE_SPEECH_KEY: Optional[str] = os.getenv("AZURE_SPEECH_KEY")
    AZURE_SPEECH_REGION: Optional[str] = os.getenv("AZURE_SPEECH_REGION")

    VOICEBOX_BASE_URL: str = os.getenv("VOICEBOX_BASE_URL", "http://127.0.0.1:17493")
    VOICEBOX_API_KEY: Optional[str] = os.getenv("VOICEBOX_API_KEY")
    VOICEBOX_DEFAULT_PROFILE_ID: Optional[str] = os.getenv("VOICEBOX_DEFAULT_PROFILE_ID")

    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "tts-bridge/voicebox")


settings = Settings()
