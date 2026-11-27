from datetime import date
from typing import Literal

from pydantic import BaseModel


class ActivityDay(BaseModel):
    date: date
    learners: int


class ActivitySeries(BaseModel):
    days: list[ActivityDay]


class Comparison(BaseModel):
    current: int
    previous: int


class FeatureRow(BaseModel):
    feature: Literal["lessons", "reading", "listening", "games", "grammar", "chat", "voice"]
    learners: int
    repeat_learners: int
    volume: int


class FeatureUsage(BaseModel):
    features: list[FeatureRow]


class ActivationCohort(BaseModel):
    week: date
    registered: int
    planned: int
    practised: int


class RetentionCohort(BaseModel):
    week: date
    started: int
    returned: int | None


class PracticePopulation(BaseModel):
    last_7: int
    days_8_30: int
    over_30: int
    never: int


class PracticeFrequency(BaseModel):
    one: int
    two_three: int
    four_seven: int
    eight_thirteen: int
    fourteen_plus: int


class WeeklyMovement(BaseModel):
    week: date
    new: int
    continuing: int
    reactivated: int
    not_returned: int


class AnalyticsSummary(BaseModel):
    weekly: Comparison
    monthly: Comparison
    repeat_weekly: Comparison
    activation: list[ActivationCohort]
    retention: list[RetentionCohort]
    population: PracticePopulation
    frequency: PracticeFrequency
    movement: list[WeeklyMovement]


class AnalyticsDetail(AnalyticsSummary):
    days: list[ActivityDay]
    features: list[FeatureRow]
