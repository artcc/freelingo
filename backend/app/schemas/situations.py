from pydantic import BaseModel


class SituationSummary(BaseModel):
    id: str
    category: str


class SituationsResponse(BaseModel):
    study_plan_id: int
    target_language: str
    cefr_level: str
    situations: list[SituationSummary]
