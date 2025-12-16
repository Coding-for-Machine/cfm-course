from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count, Q
from ninja import Router, Query
from typing import Optional

from .models import Course, Modules, Enrollment
from lessons.models import Lesson
from .schemas import CourseDetailSchema, CourseListResponseSchema
from api.utils.rate_limiter import rate_limit

router = Router(tags=["Courses"])


@router.get("/", response=CourseListResponseSchema)
def list_courses(request, search: Optional[str] = Query(None)):
    queryset = (
        Course.objects.select_related("user")
        .prefetch_related("modules")
        .annotate(
            total_lessons=Count("modules__lesson", distinct=True),
            total_modules=Count("modules", distinct=True),
            total_enrollments=Count("enrollments", distinct=True),
        )
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    enrolled_ids = set()
    if request.user.is_authenticated:
        enrolled_ids = set(
            Enrollment.objects.filter(user=request.user).values_list("course_id", flat=True)
        )

    total_courses = queryset.count()
    limit = 10
    current_page = 1
    total_pages = (total_courses + limit - 1) // limit

    courses = [
        {
            "course_id": c.id,
            "title": c.title,
            "slug": c.slug,
            "description": c.description[:200] if c.description else "",
            "instructor": c.instructor,
            "price": c.price,
            "lesson_count": c.total_lessons or 0,
            "module_count": c.total_modules,
            "enrolled_count": c.total_enrollments,
            "is_enrolled": c.id in enrolled_ids,
            "is_free": c.is_free,
            "thumbnail": c.thumbnail or (c.image.url if c.image else None),
            "created_at": c.created_at,
        }
        for c in queryset
    ]

    return {
        "success": True,
        "data": {
            "courses": courses,
            "pagination": {
                "current_page": current_page,
                "total_pages": total_pages,
                "total_courses": total_courses,
                "limit": limit,
            },
        },
    }


#  /courses/{course_id}/enroll
@router.post("/{slug}/enroll")
def enroll_course(request, slug: str):
    if not request.user.is_authenticated:
        return {"success": False, "message": "Foydalanuvchi tizimga kirmagan"}

    course = get_object_or_404(Course, slug=slug)

    if course.is_free:
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
    else:
        return {"success": False, "message": "To'lov talab qilinadi"}

    if not created:
        return {"success": False, "message": "Siz allaqachon kursga yozilgansiz"}

    return {"success": True, "message": "Kursga muvaffaqiyatli yozildingiz"}

# -------------------- Course Detail --------------------
@router.get("/{slug}", response=CourseDetailSchema)
def course_detail(request, slug: str):

    # 🔍 Kursni olish (Prefetch bilan optimallashtirilgan)
    course = get_object_or_404(
        Course.objects.select_related("user").prefetch_related(
            Prefetch(
                "modules",
                queryset=Modules.objects.prefetch_related(
                    Prefetch(
                        "lesson",
                        queryset=Lesson.objects.only(
                            "id", "title", "slug", "preview", "module_id"
                        ).order_by("created_at"),
                    )
                ).order_by("created_at"),
            )
        ),
        slug=slug,
    )

    # 👤 Foydalanuvchi kursga yozilganmi?
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    # 🧩 Modullar va darslar strukturasini tuzish
    modules_data = []
    for module in course.modules.all():
        lessons_data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "preview": lesson.preview,
            }
            for lesson in module.lesson.all()
        ]

        modules_data.append({
            "id": module.id,
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "lessons_count": len(lessons_data),
            "lessons": lessons_data,
        })

    return {
        "success": True,
        "data": {
            "course_id": course.id,
            "title": course.title,
            "slug": course.slug,
            "description": course.description,
            "price": course.price,
            "instructor": {
                "name": course.instructor,
                "avatar": course.image.url if course.image else None,
                "bio": getattr(course.user, "bio", None),
            },
            "lesson_count": course.lesson_count or 0,
            "modules": modules_data,
            "is_enrolled": is_enrolled,
            "is_free": course.is_free,
            "enrolled_count": course.enrollments.count(),
            "thumbnail": course.thumbnail or (course.image.url if course.image else None),
            "created_at": course.created_at,
            "updated_at": course.updated_at,
        },
    }

@router.get("/lesson/{slug}")
def lesson_get_slug(request, slug: str):
    lesson = get_object_or_404(Lesson.objects.prefetch_related("problems"), slug=slug)

    problems = [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "ball": p.points,
            "type": p.problem_type,
        }
        for p in lesson.problems.all()
    ]

    return {"success": True, "data": {
        "id": lesson.id,
        "title": lesson.title,
        "slug": lesson.slug,
        "pages": problems
    }}