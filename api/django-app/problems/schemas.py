# ==================== problems/schemas.py ====================
from ninja import Schema
from typing import List, Optional


# ==================== problems/schemas.py ====================
from typing import List, Optional
from pydantic import BaseModel


# -------------------- Function Schema --------------------
class FunctionSchema(BaseModel):
    language_id: int
    language_name: str
    template: str


# -------------------- Example Schema --------------------
class ExampleSchema(BaseModel):
    id: int
    input_txt: str
    output_txt: str
    explanation: Optional[str] = None


# -------------------- Hint Schema --------------------
class HintSchema(BaseModel):
    id: int
    text: str


# -------------------- Challenge Schema --------------------
class ChallengeSchema(BaseModel):
    id: int
    text: str



# -------------------- Video Schema --------------------
class VideoSchema(BaseModel):
    title: str
    slug: str
    description: Optional[str]
    hls_url: Optional[str]
    thumbnail_url: Optional[str]
    status: str
    duration: int
    views_count: int
    likes_count: int
    dislikes_count: int


# -------------------- Question / Answer Schema --------------------
class AnswerSchema(BaseModel):
    id: int
    description: str


class QuestionSchema(BaseModel):
    id: int
    description: str
    answers: List[AnswerSchema]


# -------------------- Problem List Schema --------------------
class ProblemListSchema(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: int
    points: int
    category: Optional[str] = None
    is_completed: bool
    tags: List[str]


# -------------------- Problem Detail Schema --------------------
class ProblemDetailSchema(BaseModel):
    title: str
    slug: str
    description: str
    difficulty: int
    points: int
    constraints: Optional[str] = None
    category: Optional[str] = None
    tags: List[str]
    start_function: List[FunctionSchema]
    examples: List[ExampleSchema]
    hints: List[HintSchema]
    challenges: List[ChallengeSchema]
    videos: List[VideoSchema]
    questions: List[QuestionSchema]
    is_completed: bool = False
