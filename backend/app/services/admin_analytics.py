"""Account-level analytics over retained operational records. All end dates are exclusive."""

from datetime import date, datetime, time, timedelta

from sqlalchemy import (
    Date,
    Select,
    cast,
    distinct,
    func,
    literal,
    select,
    true,
    type_coerce,
    union_all,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import ColumnElement

from app.models.chat_history import ChatHistory
from app.models.game import GameSession
from app.models.grammar_practice import GrammarPracticeSession
from app.models.lesson import Exercise, Lesson
from app.models.listening import ListeningAttempt
from app.models.progress import Progress
from app.models.reading import ReadingAttempt
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.admin_analytics import (
    ActivationCohort,
    ActivityDay,
    ActivitySeries,
    AnalyticsSummary,
    Comparison,
    FeatureRow,
    FeatureUsage,
    PracticeFrequency,
    PracticePopulation,
    RetentionCohort,
    WeeklyMovement,
)

_FEATURES = ("lessons", "reading", "listening", "games", "grammar", "chat", "voice")
# Match Python's str.strip() on both SQL dialects, including CJK and nonbreaking spaces.
_WHITESPACE = (
    " \t\n\r\f\v\x1c\x1d\x1e\x1f\x85\xa0\u1680"
    "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a"
    "\u2028\u2029\u202f\u205f\u3000"
)


def _midnight(day: date) -> datetime:
    # DateTime columns persist naive UTC.
    return datetime.combine(day, time.min)


def _monday(day: date) -> date:
    return day - timedelta(days=day.weekday())


def _add_days(db: AsyncSession, day: ColumnElement[date], days: int) -> ColumnElement[date]:
    if db.get_bind().dialect.name == "sqlite":
        return type_coerce(func.date(day, f"+{days} days"), Date)
    return day + days


async def activity_series(db: AsyncSession, end: date) -> ActivitySeries:
    start = end - timedelta(days=30)
    query = (
        select(Progress.date, func.count(distinct(Progress.user_id)))
        .join(User, User.id == Progress.user_id)
        .where(User.role == "user", Progress.date >= start, Progress.date < end)
        .group_by(Progress.date)
    )
    counts = {day: count for day, count in await db.execute(query)}
    dates = (start + timedelta(days=offset) for offset in range(30))
    return ActivitySeries(
        days=[ActivityDay(date=day, learners=counts.get(day, 0)) for day in dates]
    )


async def _population(db: AsyncSession, end: date) -> PracticePopulation:
    week = end - timedelta(days=7)
    month = end - timedelta(days=30)
    accounts = (
        select(func.max(Progress.date).label("last_day"))
        .select_from(User)
        .outerjoin(Progress, (Progress.user_id == User.id) & (Progress.date < end))
        .where(User.role == "user", User.created_at < _midnight(end))
        .group_by(User.id)
        .subquery()
    )
    last_day = accounts.c.last_day
    query = select(
        func.count().filter(last_day >= week).label("last_7"),
        func.count().filter(last_day >= month, last_day < week).label("days_8_30"),
        func.count().filter(last_day < month).label("over_30"),
        func.count().filter(last_day.is_(None)).label("never"),
    )
    return PracticePopulation(**(await db.execute(query)).mappings().one())


async def _comparisons_and_frequency(
    db: AsyncSession, end: date
) -> tuple[Comparison, Comparison, Comparison, PracticeFrequency]:
    week = end - timedelta(days=7)
    fortnight = end - timedelta(days=14)
    month = end - timedelta(days=30)
    days = (
        select(Progress.user_id, Progress.date)
        .join(User, User.id == Progress.user_id)
        .where(User.role == "user", Progress.date >= end - timedelta(days=60), Progress.date < end)
        .distinct()
        .subquery()
    )
    day = days.c.date
    accounts = (
        select(
            func.count().filter(day >= week).label("weekly"),
            func.count().filter(day >= fortnight, day < week).label("prev_week"),
            func.count().filter(day >= month).label("monthly"),
            func.count().filter(day < month).label("prev_month"),
            func.count().filter(day >= end - timedelta(days=28)).label("frequency"),
        )
        .group_by(days.c.user_id)
        .subquery()
    )
    c = accounts.c
    row = (
        await db.execute(
            select(
                func.count().filter(c.weekly > 0),
                func.count().filter(c.prev_week > 0),
                func.count().filter(c.monthly > 0),
                func.count().filter(c.prev_month > 0),
                func.count().filter(c.weekly >= 2),
                func.count().filter(c.prev_week >= 2),
                func.count().filter(c.frequency == 1).label("one"),
                func.count().filter(c.frequency.between(2, 3)).label("two_three"),
                func.count().filter(c.frequency.between(4, 7)).label("four_seven"),
                func.count().filter(c.frequency.between(8, 13)).label("eight_thirteen"),
                func.count().filter(c.frequency >= 14).label("fourteen_plus"),
            )
        )
    ).one()
    return (
        Comparison(current=row[0], previous=row[1]),
        Comparison(current=row[2], previous=row[3]),
        Comparison(current=row[4], previous=row[5]),
        PracticeFrequency(
            one=row.one,
            two_three=row.two_three,
            four_seven=row.four_seven,
            eight_thirteen=row.eight_thirteen,
            fourteen_plus=row.fourteen_plus,
        ),
    )


async def _activation(db: AsyncSession, end: date) -> list[ActivationCohort]:
    # Even Sunday's registrations need their entire D0–6 window.
    stop = _monday(end - timedelta(days=6))
    start = stop - timedelta(weeks=8)
    registered_day = type_coerce(func.date(User.created_at), Date)
    last_day = _add_days(db, registered_day, 6)
    plan_day = type_coerce(func.date(StudyPlan.created_at), Date)
    query = (
        select(
            registered_day,
            func.count(distinct(User.id)),
            func.count(distinct(StudyPlan.user_id)),
            func.count(distinct(Progress.user_id)),
        )
        .select_from(User)
        .outerjoin(
            StudyPlan,
            (StudyPlan.user_id == User.id)
            & (StudyPlan.created_at >= User.created_at)
            & (plan_day <= last_day),
        )
        .outerjoin(
            Progress,
            (Progress.study_plan_id == StudyPlan.id)
            & (Progress.user_id == User.id)
            & (Progress.date >= plan_day)
            & (Progress.date <= last_day),
        )
        .where(
            User.role == "user",
            User.created_at >= _midnight(start),
            User.created_at < _midnight(stop),
        )
        .group_by(registered_day)
    )
    cohorts = {}
    for offset in range(8):
        week = start + timedelta(weeks=offset)
        cohorts[week] = ActivationCohort(week=week, registered=0, planned=0, practised=0)
    for day, registered, planned, practised in await db.execute(query):
        cohort = cohorts[_monday(day)]
        cohort.registered += registered
        cohort.planned += planned
        cohort.practised += practised
    return list(cohorts.values())


async def _retention_and_movement(
    db: AsyncSession, end: date
) -> tuple[list[RetentionCohort], list[WeeklyMovement]]:
    stop = _monday(end)
    start = stop - timedelta(weeks=8)
    # Include the baseline week so the first displayed week has a real predecessor.
    baseline = start - timedelta(weeks=1)
    if db.get_bind().dialect.name == "sqlite":
        monday = type_coerce(func.date(Progress.date, "weekday 0", "-6 days"), Date)
    else:
        monday = cast(func.date_trunc("week", Progress.date), Date)
    active = (
        select(Progress.user_id, monday.label("week"), func.min(Progress.date).label("day"))
        .join(User, User.id == Progress.user_id)
        .where(User.role == "user", Progress.date >= baseline, Progress.date < stop)
        .group_by(Progress.user_id, "week")
        .subquery()
    )
    previous = func.lag(active.c.week).over(partition_by=active.c.user_id, order_by=active.c.week)
    history = select(active, previous.label("previous")).subquery()
    consecutive = history.c.week == _add_days(db, history.c.previous, 7)
    # Only a learner's first observed week can require a lookup in older history.
    prior = select(Progress.id).where(
        Progress.user_id == history.c.user_id, Progress.date < baseline
    )
    first = (history.c.week >= start) & history.c.previous.is_(None) & ~prior.exists()
    returned = select(Progress.id).where(
        Progress.user_id == history.c.user_id,
        Progress.date >= _add_days(db, history.c.day, 7),
        Progress.date < _add_days(db, history.c.day, 14),
    )
    last_mature = end - timedelta(days=6 + 14)
    query = select(
        history.c.week,
        func.count(),
        func.count().filter(consecutive),
        func.count().filter(first),
        func.count().filter(first, history.c.week <= last_mature, returned.exists()),
    ).group_by(history.c.week)
    totals = {row.week: row[1:] for row in await db.execute(query)}
    empty = (0, 0, 0, 0)
    previous_count = totals.get(baseline, empty)[0]
    retention = []
    movement = []
    for offset in range(8):
        week = start + timedelta(weeks=offset)
        count, continuing, started, returns = totals.get(week, empty)
        retention.append(
            RetentionCohort(
                week=week, started=started, returned=returns if week <= last_mature else None
            )
        )
        movement.append(
            WeeklyMovement(
                week=week,
                new=started,
                continuing=continuing,
                reactivated=count - continuing - started,
                not_returned=previous_count - continuing,
            )
        )
        previous_count = count
    return retention, movement


async def analytics_summary(db: AsyncSession, end: date) -> AnalyticsSummary:
    weekly, monthly, repeat_weekly, frequency = await _comparisons_and_frequency(db, end)
    retention, movement = await _retention_and_movement(db, end)
    return AnalyticsSummary(
        weekly=weekly,
        monthly=monthly,
        repeat_weekly=repeat_weekly,
        activation=await _activation(db, end),
        retention=retention,
        population=await _population(db, end),
        frequency=frequency,
        movement=movement,
    )


def _grammar_events(db: AsyncSession, start: datetime, end: datetime) -> Select:
    session = GrammarPracticeSession
    if db.get_bind().dialect.name == "sqlite":
        answers = func.json_each(session.answers).table_valued("value")
        timestamp = func.json_extract(answers.c.value, "$.answered_at")
    else:
        answers = func.json_array_elements(session.answers).table_valued("value")
        timestamp = answers.c.value.op("->>")("answered_at")
    # Extract the UTC date prefix before SQLite can round fractions up to midnight.
    day = func.date(func.substr(timestamp, 1, 10))
    # last_answered_at follows submission order, not necessarily timestamp order if
    # requests overlapped. Filter on each saved UTC ISO timestamp instead.
    return (
        select(literal("grammar"), session.user_id, literal(1), day)
        .select_from(session)
        .join(answers, true())
        .where(
            session.created_at < end,
            session.answered_count > 0,
            timestamp >= start.date().isoformat(),
            timestamp < end.date().isoformat(),
        )
    )


def _feature_day(db: AsyncSession, timestamp: ColumnElement[datetime]) -> ColumnElement[date]:
    if db.get_bind().dialect.name == "sqlite":
        # SQLAlchemy stores naive UTC as ISO text on SQLite.
        return func.substr(timestamp, 1, 10)
    return func.date(timestamp)


async def feature_usage(db: AsyncSession, end: date, days: int) -> FeatureUsage:
    if days not in (7, 30, 90):
        raise ValueError("days must be 7, 30 or 90")
    start_at = _midnight(end - timedelta(days=days))
    end_at = _midnight(end)
    # Both lesson sources contribute learners; only completed lessons contribute volume.
    lessons = (
        select(
            literal("lessons").label("feature"),
            StudyPlan.user_id,
            literal(1).label("volume"),
            _feature_day(db, Lesson.completed_at).label("day"),
        )
        .join_from(Lesson, StudyPlan, Lesson.study_plan_id == StudyPlan.id)
        .where(
            Lesson.is_completed.is_(True),
            Lesson.completed_at >= start_at,
            Lesson.completed_at < end_at,
        )
    )
    exercises = (
        select(
            literal("lessons"),
            StudyPlan.user_id,
            literal(0),
            _feature_day(db, Exercise.answered_at),
        )
        .join_from(Exercise, Lesson, Exercise.lesson_id == Lesson.id)
        .join(StudyPlan, Lesson.study_plan_id == StudyPlan.id)
        .where(Exercise.answered_at >= start_at, Exercise.answered_at < end_at)
    )
    attempts = [
        select(
            literal(feature), model.user_id, literal(1), _feature_day(db, model.completed_at)
        ).where(model.completed_at >= start_at, model.completed_at < end_at)
        for feature, model in (("reading", ReadingAttempt), ("listening", ListeningAttempt))
    ]
    games = select(
        literal("games"),
        GameSession.user_id,
        literal(1),
        _feature_day(db, GameSession.completed_at),
    ).where(
        GameSession.status == "completed",
        GameSession.completed_at >= start_at,
        GameSession.completed_at < end_at,
    )
    response = ChatHistory
    prompt = aliased(ChatHistory)
    turns = (
        select(
            response.modality, response.user_id, literal(1), _feature_day(db, response.created_at)
        )
        .join_from(response, prompt, prompt.id == response.reply_to_id)
        .where(
            response.created_at >= start_at,
            response.created_at < end_at,
            response.role == "assistant",
            prompt.role == "user",
            response.user_id == prompt.user_id,
            response.conversation_id == prompt.conversation_id,
            response.modality == prompt.modality,
            response.modality.in_(("chat", "voice")),
            func.length(func.trim(response.content, _WHITESPACE)) > 0,
            func.length(func.trim(prompt.content, _WHITESPACE)) > 0,
        )
    )
    events = union_all(
        lessons, exercises, *attempts, games, _grammar_events(db, start_at, end_at), turns
    ).subquery()
    accounts = (
        select(
            events.c.feature,
            func.sum(events.c.volume).label("volume"),
            (func.min(events.c.day) != func.max(events.c.day)).label("repeated"),
        )
        .join(User, User.id == events.c.user_id)
        .where(User.role == "user")
        .group_by(events.c.feature, events.c.user_id)
        .subquery()
    )
    query = select(
        accounts.c.feature,
        func.count(),
        func.sum(accounts.c.volume),
        func.count().filter(accounts.c.repeated),
    ).group_by(accounts.c.feature)
    rows = {
        feature: (learners, volume, repeat_learners)
        for feature, learners, volume, repeat_learners in await db.execute(query)
    }
    features = []
    for feature in _FEATURES:
        learners, volume, repeat_learners = rows.get(feature, (0, 0, 0))
        features.append(
            FeatureRow(
                feature=feature, learners=learners, volume=volume, repeat_learners=repeat_learners
            )
        )
    features.sort(key=lambda row: -row.learners)
    return FeatureUsage(features=features)
