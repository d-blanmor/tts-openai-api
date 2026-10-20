from typing import Literal, Optional

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    model: str = Field(..., description="Model alias exposed to Open WebUI")
    input: str = Field(..., description="Text to synthesize")
    voice: Optional[str] = Field(default=None, description="Voice name or identifier")
    response_format: Literal["mp3", "wav", "opus", "aac"] = Field(
        default="mp3",
        description="Audio output format",
    )
    speed: float = Field(default=1.0, ge=0.25, le=4.0)


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    owned_by: str = "tts-bridge"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: list[ModelInfo]
