# ==================== courses/schemas.py ====================
from ninja import Schema
from typing import Optional, List
from datetime import datetime


# -------------------- Course List Schema --------------------
# ==================== courses/schemas.py ====================

# -------------------- Ichki schema (kurs ma'lumotlari) --------------------
class CourseItemSchema(Schema):
    course_id: int
    title: str
    slug: str
    description: Optional[str] = None
    instructor: str
    price: int
    lesson_count: int
    module_count: int
    enrolled_count: int
    is_enrolled: bool
    is_free: bool
    thumbnail: Optional[str] = None
    created_at: datetime


# -------------------- Pagination schema --------------------
class PaginationSchema(Schema):
    current_page: int
    total_pages: int
    total_courses: int
    limit: int


# -------------------- Asosiy schema (API javobi) --------------------
class CourseListSchema(Schema):
    success: bool
    data: dict  # yoki pastdagi to‘liq struktura sifatida yozish mumkin


# Agar siz `data` ichidagi tuzilmani ham to‘liq schema bilan ko‘rsatmoqchi bo‘lsangiz:
class CourseListResponseSchema(Schema):
    success: bool
    data: "CourseListDataSchema"


class CourseListDataSchema(Schema):
    courses: List[CourseItemSchema]
    pagination: PaginationSchema



# -------------------- Course Detail Schema --------------------
class LessonSchema(Schema):
    id: int
    title: str
    slug: str
    preview: bool


class ModuleSchema(Schema):
    id: int
    title: str
    slug: str
    description: Optional[str]
    lessons_count: int
    lessons: List[LessonSchema]


class InstructorSchema(Schema):
    name: str
    avatar: Optional[str]
    bio: Optional[str]


class CourseDetailDataSchema(Schema):
    course_id: int
    title: str
    slug: str
    description: Optional[str]
    price: int
    instructor: InstructorSchema
    lesson_count: int
    modules: List[ModuleSchema]
    is_enrolled: bool
    is_free: bool
    enrolled_count: int
    thumbnail: Optional[str]
    created_at: datetime
    updated_at: datetime


class CourseDetailSchema(Schema):
    success: bool
    data: CourseDetailDataSchema
