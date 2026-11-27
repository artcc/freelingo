from datetime import date, datetime, time, timedelta
from uuid import uuid4

from app.core.database import get_db
from app.core.security import create_access_token
from app.main import app
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.game import GameSession
from app.models.grammar_practice import GrammarPracticeSession, GrammarPracticeTopic
from app.models.lesson import Exercise, Lesson
from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.progress import Progress
from app.models.reading import ReadingAttempt, ReadingExercise
from app.models.user import User
from app.routers import admin_analytics as analytics_router
from app.services import admin_analytics
from app.services.admin_analytics import activity_series, analytics_summary, feature_usage
from tests import test_progress_rewards_postgres as postgres_helpers
from tests.conftest import make_study_plan

postgres_sessions = postgres_helpers.postgres_sessions

END = date(2026, 11, 27)  # Friday
DAY = timedelta(days=1)
FEATURES = {"lessons", "reading", "listening", "games", "grammar", "chat", "voice"}


def midnight(day):
    return datetime.combine(day, time.min)


async def account(db, name, joined):
    user = User(
        username=name,
        display_name=name,
        hashed_password="unused",
        native_language="es",
        created_at=midnight(joined),
    )
    db.add(user)
    await db.flush()
    return user


async def plan_for(db, user, *, language="en-GB", created=None):
    return await make_study_plan(
        db,
        user_id=user.id,
        target_language=language,
        cefr_level="A1",
        created_at=created or user.created_at,
    )


def practice(db, plan, *days):
    db.add_all(
        Progress(user_id=plan.user_id, study_plan_id=plan.id, date=day, xp_earned=0) for day in days
    )


def feature_counts(result):
    assert len(result.features) == len(FEATURES)
    counts = {
        row.feature: (row.learners, row.volume, row.repeat_learners) for row in result.features
    }
    assert counts.keys() == FEATURES
    return counts


async def test_activity_and_comparisons_count_accounts_and_distinct_utc_days(
    db_session, admin_user
):
    db = db_session
    registered = END - 100 * DAY
    regular = await account(db, "regular", registered)
    en = await plan_for(db, regular)
    fr = await plan_for(db, regular, language="fr")
    practice(db, en, END - 14 * DAY, END - 8 * DAY, END - 7 * DAY, END - DAY)
    practice(db, fr, END - DAY)

    once = await account(db, "once", registered)
    once.is_active = False
    practice(db, await plan_for(db, once), END - DAY)
    practice(db, await plan_for(db, once, language="fr"), END - DAY)
    previous = await account(db, "previous", registered)
    practice(db, await plan_for(db, previous), END - 8 * DAY, END - 12 * DAY, END - 30 * DAY)
    previous_only = await account(db, "previous-only", registered)
    practice(db, await plan_for(db, previous_only), END - 14 * DAY)
    old = await account(db, "old", registered)
    practice(db, await plan_for(db, old), END - 31 * DAY, END - 60 * DAY)
    outside = await account(db, "outside", registered)
    practice(db, await plan_for(db, outside), END - 61 * DAY, END)
    practice(db, await plan_for(db, admin_user[0]), END - DAY, END)
    await db.flush()

    series = await activity_series(db, END)
    days = [row.date for row in series.days]
    assert days == [END - n * DAY for n in range(30, 0, -1)]
    observed = {row.date: row.learners for row in series.days}
    assert observed[END - DAY] == 2
    assert observed[END - 2 * DAY] == 0
    assert observed[END - 7 * DAY] == 1
    assert observed[END - 8 * DAY] == 2
    assert observed[END - 30 * DAY] == 1

    summary = await analytics_summary(db, END)
    assert (summary.weekly.current, summary.weekly.previous) == (2, 3)
    assert (summary.monthly.current, summary.monthly.previous) == (4, 1)
    assert (summary.repeat_weekly.current, summary.repeat_weekly.previous) == (1, 2)


async def test_account_distribution_uses_latest_practice_and_only_complete_days(
    db_session, admin_user
):
    db = db_session
    for name, ages in (
        ("yesterday", (31, 1)),
        ("one-week", (7,)),
        ("eight-days", (8,)),
        ("month-end", (30, 0)),
        ("long-absent", (31,)),
        ("first-practice-today", (0,)),
        ("no-plan", ()),
    ):
        user = await account(db, name, END - 90 * DAY)
        if name == "one-week":
            user.is_active = False
        if ages:
            practice(db, await plan_for(db, user), *(END - age * DAY for age in ages))
    await account(db, "signed-up-today", END)
    practice(db, await plan_for(db, admin_user[0]), END - DAY)
    await db.flush()
    population = (await analytics_summary(db, END)).population
    assert population.model_dump() == {"last_7": 2, "days_8_30": 2, "over_30": 1, "never": 2}


async def test_frequency_histogram_buckets_distinct_days_per_learner(db_session):
    db = db_session
    for n in (0, 1, 2, 3, 4, 7, 8, 13, 14, 28):
        user = await account(db, f"frequency-{n}", END - 91 * DAY)
        plan = await plan_for(db, user)
        practice(db, plan, END - 29 * DAY, END, *(END - d * DAY for d in range(1, n + 1)))
        if n:
            practice(db, await plan_for(db, user, language="fr"), END - DAY)
    await db.flush()
    result = (await analytics_summary(db, END)).frequency
    assert result.model_dump() == {
        "one": 1,
        "two_three": 2,
        "four_seven": 2,
        "eight_thirteen": 2,
        "fourteen_plus": 2,
    }


async def test_weekly_movement_reconciles_with_previous_week_across_year_and_languages(db_session):
    db = db_session
    cutoff = date(2027, 2, 3)  # Wednesday; the current week is excluded.
    start = date(2026, 12, 7)
    for name, offsets in (
        ("new", (6, 7, 14)),
        ("continuous", (-1, 0, 1)),
        ("returning", (-200, 0, 14)),
        ("lapsed", (-7,)),
        ("gap", (-8, 7)),
        ("outside", (56,)),
    ):
        user = await account(db, name, start - 250 * DAY)
        practice(db, await plan_for(db, user), *(start + d * DAY for d in offsets))
        if name == "new":
            practice(db, await plan_for(db, user, language="fr"), start + 6 * DAY)
    await db.flush()
    rows = (await analytics_summary(db, cutoff)).movement
    assert [r.week for r in rows] == [start + 7 * i * DAY for i in range(8)]
    assert [(r.new, r.continuing, r.reactivated, r.not_returned) for r in rows] == [
        (1, 1, 1, 1),
        (0, 1, 1, 2),
        (0, 1, 1, 1),
        (0, 0, 0, 2),
        *[(0, 0, 0, 0)] * 4,
    ]


async def test_activation_counts_ordered_steps_within_registration_days_zero_to_six(
    db_session, admin_user
):
    db = db_session
    week = date(2026, 10, 26)
    sunday = week + 6 * DAY

    activated = await account(db, "activated", sunday)
    activated.created_at = datetime.combine(sunday, time(23, 59))
    en = await plan_for(db, activated)
    fr = await plan_for(db, activated, language="fr", created=midnight(sunday + DAY))
    practice(db, en, sunday, sunday + 6 * DAY)
    practice(db, fr, sunday + 6 * DAY)
    last_day = await account(db, "last-day", week)
    timely_plan = await plan_for(db, last_day, created=midnight(week + 6 * DAY))
    timely_plan.is_active = False
    practice(db, timely_plan, week + 6 * DAY)
    early_practice = await account(db, "early-practice", week)
    later_plan = await plan_for(db, early_practice, created=midnight(week + 2 * DAY))
    practice(db, later_plan, week + DAY)
    missed_practice = await account(db, "missed-practice", week)
    practice(db, await plan_for(db, missed_practice), week + 7 * DAY)
    late = await account(db, "late-plan", week)
    late_plan = await plan_for(db, late, created=midnight(week + 7 * DAY))
    practice(db, late_plan, week + 7 * DAY)
    await account(db, "registered-only", week)
    admin = admin_user[0]
    admin.created_at = midnight(week)
    practice(db, await plan_for(db, admin), week)
    await db.flush()

    rows = (await analytics_summary(db, END)).activation
    last_mature_week = date(2026, 11, 9)
    expected_weeks = [last_mature_week - timedelta(weeks=n) for n in reversed(range(8))]
    assert [row.week for row in rows] == expected_weeks
    row = next(row for row in rows if row.week == week)
    assert (row.registered, row.planned, row.practised) == (6, 4, 2)
    assert all((r.registered, r.planned, r.practised) == (0, 0, 0) for r in rows if r != row)


async def test_retention_uses_first_global_practice_and_days_seven_through_thirteen(
    db_session, admin_user
):
    db = db_session
    week = date(2026, 10, 26)
    for name, start, returns in (
        ("day-seven", week, [7]),
        ("several-returns", week, [7, 8, 13]),
        ("day-thirteen", week + 6 * DAY, [13]),
        ("too-early", week, [6]),
        ("too-late", week + DAY, [14]),
        ("immature-cohort", date(2026, 11, 9), [7]),
        ("recent", date(2026, 11, 22), []),
    ):
        user = await account(db, name, week - 90 * DAY)
        practice(db, await plan_for(db, user), start)
        other_language = await plan_for(db, user, language="fr")
        practice(db, other_language, start, *(start + n * DAY for n in returns))
    existing = await account(db, "existing", week - 100 * DAY)
    practice(db, await plan_for(db, existing), week - 90 * DAY, week, week + 8 * DAY)
    practice(db, await plan_for(db, admin_user[0]), week, week + 7 * DAY)
    await db.flush()

    rows = (await analytics_summary(db, END)).retention
    last_full_week = date(2026, 11, 16)
    assert [row.week for row in rows] == [last_full_week - n * 7 * DAY for n in reversed(range(8))]
    mature = next(row for row in rows if row.week == week)
    assert (mature.started, mature.returned) == (5, 3)
    assert (rows[-2].started, rows[-2].returned) == (1, None)
    assert (rows[-1].started, rows[-1].returned) == (1, None)


def lesson(plan, title, completed_at):
    return Lesson(
        study_plan_id=plan.id,
        title=title,
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        is_completed=completed_at is not None,
        completed_at=completed_at,
    )


async def test_feature_usage_counts_completions_and_attempts_not_generation_or_xp(
    db_session, test_user, admin_user
):
    db = db_session
    en = await plan_for(db, test_user[0])
    fr = await plan_for(db, test_user[0], language="fr")
    admin = await plan_for(db, admin_user[0])
    start = midnight(END - 7 * DAY)
    stop = midnight(END)
    before = start - timedelta(microseconds=1)
    last = stop - timedelta(microseconds=1)
    pending = lesson(fr, "pending", None)
    db.add_all(
        [
            lesson(en, "first", start),
            lesson(fr, "same day in French", start + timedelta(hours=3)),
            pending,
            lesson(fr, "before", before),
            lesson(fr, "after", stop),
            lesson(admin, "admin", start),
        ]
    )
    common = dict(level="A1", target_language=en.target_language, topic="Travel", questions=[])
    reading = ReadingExercise(**common, text="Article", exercise_type="article", view_count=40)
    listening = ListeningExercise(
        **common, text="Story", exercise_type="story", audio_path="story.wav", play_count=20
    )
    db.add_all([reading, listening])
    await db.flush()
    second_user = await account(db, "second-reader", END - 30 * DAY)
    second = await plan_for(db, second_user)
    partial = lesson(second, "exercise only", None)
    second_fr = await plan_for(db, second_user, language="fr")
    db.add_all([partial, lesson(second_fr, "previous week", before)])
    await db.flush()
    for parent, answered_at in ((pending, start + timedelta(hours=2)), (partial, last)):
        db.add(
            Exercise(
                lesson_id=parent.id,
                exercise_type="translation",
                question="Translate",
                correct_answer="Hello",
                user_answer="Hello",
                answered_at=answered_at,
            )
        )
    for model, exercise, attempts in (
        (
            ReadingAttempt,
            reading,
            [(en, start), (en, last), (second, start), (en, stop - 40 * DAY)],
        ),
        (ListeningAttempt, listening, [(en, start)]),
    ):
        for plan, when in [*attempts, (admin, start), (admin, last), (en, before), (en, stop)]:
            db.add(
                model(
                    user_id=plan.user_id,
                    study_plan_id=plan.id,
                    exercise_id=exercise.id,
                    answers={},
                    score=0,
                    xp_earned=0,
                    completed_at=when,
                )
            )
    for plan, status, completed in (
        (en, "completed", last),
        (fr, "completed", start),
        (fr, "abandoned", None),
        (en, "completed", before),
        (admin, "completed", start),
    ):
        db.add(
            GameSession(
                id=str(uuid4()),
                user_id=plan.user_id,
                study_plan_id=plan.id,
                mode="free",
                target_language=plan.target_language,
                native_language="es",
                level="A1",
                status=status,
                created_at=before,
                deadline=stop,
                completed_at=completed,
            )
        )
    await db.flush()

    counts = feature_counts(await feature_usage(db, END, 7))
    assert counts == {
        "lessons": (2, 2, 0),
        "reading": (2, 3, 1),
        "listening": (1, 1, 0),
        "games": (1, 2, 1),
        "grammar": (0, 0, 0),
        "chat": (0, 0, 0),
        "voice": (0, 0, 0),
    }
    wider = feature_counts(await feature_usage(db, END, 30))
    assert wider["lessons"] == (2, 4, 2)
    assert wider["reading"] == (2, 4, 1)
    assert wider["listening"] == (1, 2, 1)
    assert feature_counts(await feature_usage(db, END, 90))["reading"] == (2, 5, 1)


async def seed_grammar_answers(db, plan):
    topic = GrammarPracticeTopic(
        user_language_id=plan.user_language_id,
        grammar_slug="articles",
        created_at=midnight(END - 8 * DAY),
    )
    db.add(topic)
    await db.flush()
    start = midnight(END - 7 * DAY)
    stop = midnight(END)
    boundary = start + DAY
    for times in (
        [boundary - timedelta(microseconds=1), start - timedelta(microseconds=1)],
        [boundary, boundary + timedelta(seconds=10), boundary + timedelta(seconds=20), stop],
    ):
        db.add(
            GrammarPracticeSession(
                id=str(uuid4()),
                topic_id=topic.id,
                user_id=plan.user_id,
                study_plan_id=plan.id,
                target_language=plan.target_language,
                native_language="es",
                topic_level="A1",
                learner_level="A1",
                title="Articles",
                topic_snapshot={},
                answers=[
                    {"index": i, "value": 0, "correct": False, "answered_at": ts.isoformat() + "Z"}
                    for i, ts in enumerate(times)
                ],
                answered_count=len(times),
                last_answered_at=times[-1],
                status="abandoned",
                created_at=min(times) - timedelta(minutes=2),
                deadline=times[0] + timedelta(minutes=5),
            )
        )
    await db.flush()


async def test_grammar_uses_each_json_answer_timestamp_not_session_totals(db_session, test_user):
    await seed_grammar_answers(db_session, await plan_for(db_session, test_user[0]))
    assert feature_counts(await feature_usage(db_session, END, 7))["grammar"] == (1, 4, 1)


async def test_report_with_postgres_dates_and_json(postgres_sessions):
    async with postgres_sessions() as db:
        monday = date(2026, 10, 26)
        user = await account(db, "learner", monday)
        plan = await plan_for(db, user)
        practice(db, plan, monday, monday + 13 * DAY)
        await seed_grammar_answers(db, plan)
        report = await analytics_summary(db, END)
        assert report.population.days_8_30 == 1
        assert report.frequency.one == 1
        first_week = next(row for row in report.movement if row.week == monday)
        second_week = next(row for row in report.movement if row.week == monday + 7 * DAY)
        assert (first_week.new, first_week.reactivated, second_week.continuing) == (1, 0, 1)
        activation = next(row for row in report.activation if row.week == monday)
        assert (activation.registered, activation.planned, activation.practised) == (1, 1, 1)
        retention = next(row for row in report.retention if row.week == monday)
        assert (retention.started, retention.returned) == (1, 1)
        assert feature_counts(await feature_usage(db, END, 7))["grammar"] == (1, 4, 1)


async def test_postgres_report_keeps_one_snapshot_during_plan_deletion(
    postgres_sessions, client, monkeypatch
):
    async with postgres_sessions() as db:
        admin = await account(db, "report-admin", END - 30 * DAY)
        admin.role = "admin"
        learner = await account(db, "snapshot-learner", END - 30 * DAY)
        plan = await plan_for(db, learner)
        practice(db, plan, END - DAY)
        await db.commit()
        token = create_access_token(admin.id, admin.role)

    async def report_db():
        async with postgres_sessions() as reader:
            yield reader

    population = admin_analytics._population

    async def delete_then_measure(reader, end):
        async with postgres_sessions() as writer:
            await writer.delete(plan)
            await writer.commit()
        return await population(reader, end)

    monkeypatch.setitem(app.dependency_overrides, get_db, report_db)
    monkeypatch.setattr(analytics_router, "progress_today", lambda: END)
    monkeypatch.setattr(admin_analytics, "_population", delete_then_measure)
    response = await client.get(
        "/api/admin/analytics", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    report = response.json()
    assert report["weekly"]["current"] == report["population"]["last_7"] == 1
    assert report["population"]["never"] == 0


async def test_conversation_features_split_same_thread_by_turn_modality(db_session, test_user):
    db = db_session
    plan = await plan_for(db, test_user[0])
    thread = Conversation(
        user_id=plan.user_id,
        study_plan_id=plan.id,
        target_language=plan.target_language,
        source="chat",
    )
    db.add(thread)
    await db.flush()
    start = midnight(END - 7 * DAY)
    stop = midnight(END)
    fields = dict(
        conversation_id=thread.id,
        study_plan_id=plan.id,
        user_id=plan.user_id,
        target_language=plan.target_language,
    )
    for mode, reply_mode, reply_at, content in (
        ("chat", "chat", start, "Hello"),
        ("chat", "chat", start + timedelta(hours=2), "Another question"),
        ("voice", "voice", start, "Hello"),
        ("voice", "voice", stop - timedelta(microseconds=1), "Goodbye"),
        (None, None, start, "Legacy"),
        ("chat", "voice", start, "Wrong modality"),
        ("voice", "voice", start, " \n"),
        ("voice", "voice", start, "\u3000"),
        ("chat", "chat", start, "Reply to a blank prompt"),
        ("chat", "chat", stop, "Today"),
    ):
        prompt = ChatHistory(
            **fields,
            role="user",
            content="\u3000" if content == "Reply to a blank prompt" else "Hi",
            modality=mode,
            created_at=reply_at - timedelta(seconds=1),
        )
        db.add(prompt)
        await db.flush()
        db.add(
            ChatHistory(
                **fields,
                role="assistant",
                content=content,
                modality=reply_mode,
                created_at=reply_at,
                reply_to_id=prompt.id,
            )
        )
    db.add(
        ChatHistory(**fields, role="assistant", content="Hi!", modality="voice", created_at=start)
    )
    db.add(ChatHistory(**fields, role="user", content="Hello?", modality="chat", created_at=start))
    await db.flush()
    counts = feature_counts(await feature_usage(db, END, 7))
    assert counts["chat"] == (1, 2, 0)
    assert counts["voice"] == (1, 2, 1)


async def test_empty_database_returns_zero_filled_metrics(db_session):
    series = await activity_series(db_session, END)
    assert series.days and all(row.learners == 0 for row in series.days)
    summary = await analytics_summary(db_session, END)
    for metric in (summary.weekly, summary.monthly, summary.repeat_weekly):
        assert (metric.current, metric.previous) == (0, 0)
    assert all((r.registered, r.planned, r.practised) == (0, 0, 0) for r in summary.activation)
    for row in summary.retention:
        assert row.started == 0
        assert row.returned == (0 if row.week + 20 * DAY <= END else None)
    counts = feature_counts(await feature_usage(db_session, END, 7))
    assert all(count == (0, 0, 0) for count in counts.values())
