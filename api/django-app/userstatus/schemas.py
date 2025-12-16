from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, List



class ActivitySchema(BaseModel):
    id: int
    date: date
    activity_count: int
    total_duration: int  # minutes
    score: int
    problem_solved: int

class BadgeSchema(BaseModel):
    name: str
    description: str
    icon: str
    badge_type: str
    threshold: int
    color: str

class UserBadgeSchema(BaseModel):
    id: int
    badge: BadgeSchema
    date_earned: datetime
    progress: float

class UserProblemStatusSchema(BaseModel):
    problem_id: int
    problem_title: str
    is_completed: bool
    score: int

class UserStatsSchema(BaseModel):
    total_solved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    total_score: int
    current_streak: int
    max_streak: int
    last_activity: Optional[datetime]

class ContributionDaySchema(BaseModel):
    date: date
    count: int

class ContributionMonthSchema(BaseModel):
    month: str
    days: List[ContributionDaySchema]

class ContributionCalendarSchema(BaseModel):
    year: int
    total: int
    calendar: List[ContributionMonthSchema]


