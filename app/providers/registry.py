from app.config import settings
from app.providers.azure import AzureTTSProvider
from app.providers.elevenlabs import ElevenLabsProvider
from app.providers.google import GoogleTTSProvider
from app.providers.voicebox import VoiceBoxProvider

PROVIDER_MAP = {
    "tts-bridge/elevenlabs": ElevenLabsProvider(),
    "tts-bridge/google": GoogleTTSProvider(),
    "tts-bridge/azure": AzureTTSProvider(),
    "tts-bridge/voicebox": VoiceBoxProvider(),
    "elevenlabs": ElevenLabsProvider(),
    "google": GoogleTTSProvider(),
    "azure": AzureTTSProvider(),
    "voicebox": VoiceBoxProvider(),
}


def get_provider(model_name: str):
    normalized = (model_name or "").strip().lower()

    if not normalized:
        return get_provider(settings.DEFAULT_PROVIDER)

    provider = PROVIDER_MAP.get(normalized)
    if provider is not None:
        return provider

    if normalized.startswith("tts-bridge/"):
        provider = PROVIDER_MAP.get(normalized.replace("tts-bridge/", ""))
        if provider is not None:
            return provider

    fallback = (settings.DEFAULT_PROVIDER or "").strip()
    if fallback and fallback.lower() != normalized:
        try:
            return get_provider(fallback)
        except ValueError:
            pass

    raise ValueError(f"Unsupported model: {model_name}")
