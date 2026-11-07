from fastapi import APIRouter, Depends, Query, Request

from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.data._types import CurriculumUnit
from app.data.curriculum import get_curriculum, get_curriculum_units
from app.models.user import User
from app.schemas.curriculum import CurriculumResponse, CurriculumUnitResponse

router = APIRouter(prefix="/api/curriculum", tags=["curriculum"])


def _to_response(u: CurriculumUnit) -> dict:
    return CurriculumUnitResponse(
        id=u.id,
        level=u.level,
        unit_number=u.unit_number,
        title=u.title,
        default_weeks=u.default_weeks,
        grammar_points=u.grammar_points,
        vocabulary_set_ids=u.vocabulary_set_ids,
        lesson_types=list(u.lesson_types),
        prerequisite_unit=u.prerequisite_unit,
        competency_checklist=u.competency_checklist,
    )


@router.get("", response_model=CurriculumResponse)
@limiter.limit("60/minute")
def get_all_curriculum(
    request: Request,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
) -> dict:
    curriculum = get_curriculum(language)
    return {
        "A1": [_to_response(u) for u in curriculum["A1"]],
        "A2": [_to_response(u) for u in curriculum["A2"]],
        "B1": [_to_response(u) for u in curriculum["B1"]],
        "B2": [_to_response(u) for u in curriculum["B2"]],
        "C1": [_to_response(u) for u in curriculum["C1"]],
        "C2": [_to_response(u) for u in curriculum["C2"]],
    }


@router.get("/{level}", response_model=list[CurriculumUnitResponse])
@limiter.limit("60/minute")
def get_curriculum_by_level(
    request: Request,
    level: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
) -> list:
    units = get_curriculum_units(level, language)
    return [_to_response(u) for u in units]
