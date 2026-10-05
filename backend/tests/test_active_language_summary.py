from datetime import date

import pytest
from sqlalchemy import select

from app.models.progress import Progress
from app.models.user_language import UserLanguage
from tests.conftest import make_study_plan


@pytest.mark.asyncio
async def test_switching_active_language_keeps_summary_on_current_plan(client, test_user, db_session):
    user, headers = test_user
    english = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        is_active=True,
    )
    spanish = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="es-ES",
        cefr_level="A1",
        is_active=True,
    )
    db_session.add_all([
        Progress(user_id=user.id, study_plan_id=english.id, date=date.today(), xp_earned=190, skills={}),
        Progress(user_id=user.id, study_plan_id=spanish.id, date=date.today(), xp_earned=7, skills={}),
    ])
    await db_session.commit()

    switched = await client.put(
        "/api/languages/active",
        headers=headers,
        json={"target_language": "es-ES"},
    )
    assert switched.status_code == 200

    active_rows = (
        await db_session.execute(
            select(UserLanguage).where(
                UserLanguage.user_id == user.id,
                UserLanguage.is_active.is_(True),
            )
        )
    ).scalars().all()
    assert [row.target_language for row in active_rows] == ["es-ES"]

    summary = await client.get("/api/progress/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_xp"] == 7
