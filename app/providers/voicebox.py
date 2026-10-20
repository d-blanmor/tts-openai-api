import shutil
import subprocess
import tempfile
from pathlib import Path

import httpx

from app.config import settings
from app.providers.base import BaseTTSProvider


class VoiceBoxProvider(BaseTTSProvider):
    name = "voicebox"
    default_voice = None

    async def synthesize(
        self,
        text: str,
        voice: str | None,
        response_format: str,
        speed: float,
    ) -> bytes:
        if not text or not text.strip():
            raise ValueError("Text input is required for VoiceBox synthesis.")

        profile_id = await self._resolve_profile_id(voice)
        payload = {
            "profile_id": profile_id,
            "text": text,
            "language": "en",
            "engine": "kokoro",
            "normalize": True,
        }

        headers = {"Content-Type": "application/json"}
        if settings.VOICEBOX_API_KEY:
            headers["Authorization"] = f"Bearer {settings.VOICEBOX_API_KEY}"

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{settings.VOICEBOX_BASE_URL.rstrip('/')}/generate/stream",
                json=payload,
                headers=headers,
            )

        if response.status_code >= 400:
            detail = response.text[:500]
            raise RuntimeError(f"VoiceBox request failed ({response.status_code}): {detail}")

        wav_bytes = response.content
        if response_format == "wav":
            return wav_bytes

        if response_format == "mp3":
            return await self._convert_wav_to_mp3(wav_bytes)

        if response_format in {"opus", "aac"}:
            return wav_bytes

        return wav_bytes

    async def _resolve_profile_id(self, voice: str | None) -> str:
        headers = {}
        if settings.VOICEBOX_API_KEY:
            headers["Authorization"] = f"Bearer {settings.VOICEBOX_API_KEY}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.VOICEBOX_BASE_URL.rstrip('/')}/profiles",
                headers=headers,
            )

        if response.status_code >= 400:
            raise RuntimeError(f"VoiceBox profile lookup failed: {response.text}")

        profiles = response.json()
        if not profiles:
            raise RuntimeError("VoiceBox returned no profiles. Create a profile first.")

        if settings.VOICEBOX_DEFAULT_PROFILE_ID:
            for profile in profiles:
                if str(profile.get("id")) == settings.VOICEBOX_DEFAULT_PROFILE_ID:
                    return str(profile["id"])

        if voice:
            voice_value = str(voice).strip()
            for profile in profiles:
                if str(profile.get("id")) == voice_value:
                    return str(profile["id"])
                if str(profile.get("name", "")).lower() == voice_value.lower():
                    return str(profile["id"])

        if voice:
            for profile in profiles:
                if str(profile.get("name", "")).lower().startswith(voice.lower()):
                    return str(profile["id"])

        default_profile = profiles[0]
        return str(default_profile["id"])

    async def _convert_wav_to_mp3(self, wav_bytes: bytes) -> bytes:
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            raise RuntimeError(
                "VoiceBox returned WAV but ffmpeg is not installed; mp3 conversion is unavailable. "
                "Use response_format='wav' or install ffmpeg."
            )

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "voicebox.wav"
            output_path = Path(tmp_dir) / "voicebox.mp3"
            input_path.write_bytes(wav_bytes)

            subprocess.run(
                [
                    ffmpeg_path,
                    "-y",
                    "-i",
                    str(input_path),
                    "-vn",
                    "-codec:a",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
            )
            return output_path.read_bytes()
