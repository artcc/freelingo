from pydantic import BaseModel, Field, field_validator


class QuestionExplanationContent(BaseModel):
    explanation: str = Field(min_length=1, max_length=1200)
    evidence: str = Field(min_length=1, max_length=1500)

    @field_validator("explanation", "evidence", mode="before")
    @classmethod
    def trim_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class QuestionExplanationResponse(QuestionExplanationContent):
    native_language: str
    target_language: str
