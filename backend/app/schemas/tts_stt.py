from typing import Self

from pydantic import BaseModel, Field, model_validator


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    voice: str | None = None


class ContextualTTSRequest(TTSRequest):
    study_plan_id: int | None = Field(default=None, strict=True, gt=0, le=2_147_483_647)
    conversation_id: int | None = Field(default=None, strict=True, gt=0, le=2_147_483_647)

    @model_validator(mode="after")
    def validate_context(self) -> Self:
        if self.study_plan_id is not None and self.conversation_id is not None:
            raise ValueError("Provide either study_plan_id or conversation_id, not both")
        return self


class STTResponse(BaseModel):
    text: str
