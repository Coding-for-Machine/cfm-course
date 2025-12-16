# ==================== api/problems.py ====================
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Prefetch
from typing import List, Optional
from django.core.paginator import Paginator

from problems.models import Problem, Function, Language, Category, Hint, Challenge, Examples, Video, VideoQuality
from api.utils.auth import JWTAuth
from api.utils.rate_limiter import rate_limit
from problems.schemas import *
from quizs.models import Question
from utils.auth import JWTBearer

router = Router(tags=["Problems"])




@router.get("/")
def list_problems(
    request,
    page: int = 1,
    page_size: int = 20,
    difficulty: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
):

    queryset = Problem.objects.filter(is_active=True) \
        .select_related("category") \
        .prefetch_related("tags", "language")

    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)
    if category:
        queryset = queryset.filter(category__slug=category)
    if language:
        queryset = queryset.filter(language__name=language)
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        queryset = queryset.filter(tags__name__in=tag_list).distinct()

    # Foydalanuvchi bajargan masalalar
    user_completed = set()
    if request.user.is_authenticated:
        from userstatus.models import UserProblemStatus

        user_completed = set(
            UserProblemStatus.objects.filter(
                user=request.user, is_completed=True
            ).values_list("problem_id", flat=True)
        )

    # ---------------- PAGINATION ----------------
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    results = [
        {
            "title": p.title,
            "slug": p.slug,
            "difficulty": p.difficulty,
            "points": p.points,
            "category": p.category.name if p.category else None,
            "is_completed": p.id in user_completed,
            "tags": [t.name for t in p.tags.all()],
        }
        for p in page_obj
    ]

    return {
        "page": page_obj.number,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "results": results,
    }

# -------------------- Problem Detail --------------------
@router.get("/{slug}", response=ProblemDetailSchema, auth=JWTBearer())
def get_problem(request, slug: str):
    """
    Ma’lumotlarni to‘liq qaytaradi:
    - Problem asosiy ma’lumotlari
    - Tags, languages, examples, hints, challenges
    - Video va ularning sifatlari (qualities)
    - Start function har bir til bo‘yicha
    """
    problem = get_object_or_404(
        Problem.objects.select_related("category").prefetch_related(
            "tags",
            Prefetch("examples", queryset=Examples.objects.all()),
            Prefetch("hints", queryset=Hint.objects.only("id", "text")),
            Prefetch("challenges", queryset=Challenge.objects.only("id", "text")),
            Prefetch("videos", queryset=Video.objects.prefetch_related(
                Prefetch("qualities", queryset=VideoQuality.objects.all())
            )),
            Prefetch("functions", queryset=Function.objects.select_related("language"))
        ),
        slug=slug,
        is_active=True,
    )

    # Foydalanuvchi bajargan masalalar
    user_completed = set()
    if request.user.is_authenticated:
        from userstatus.models import UserProblemStatus
        user_completed = set(
            UserProblemStatus.objects.filter(user=request.user, is_completed=True)
            .values_list("problem_id", flat=True)
        )

    # Questions and answers
    problem_questions = Question.objects.filter(problems=problem).prefetch_related("answers")
    question_data = [
        {
            "id": q.id,
            "description": q.description,
            "answers": [{"id": a.id, "description": a.description} for a in q.answers.all()]
        }
        for q in problem_questions
    ]

    # Videos
    videos_data = []
    for video in problem.videos.all():
        try:
            videos_data.append({
                "title": video.title,
                "slug": video.slug,
                "description": video.description,
                "hls_url": video.get_hls_url(),
                "thumbnail_url": video.get_thumbnail_url(),
                "duration": video.duration,
                "views_count": video.views_count,
                "likes_count": video.likes_count,
                "dislikes_count": video.dislikes_count,
            })
        except Exception:
            continue

    # Start function: language bo‘yicha shablon
    start_functions = [
        {
            "language_id": f.language.id,
            "language_name": f.language.name,
            "template": f.function
        }
        for f in problem.functions.all()
    ]

    # API Response
    return {
        "title": problem.title,
        "slug": problem.slug,
        "description": problem.description,
        "difficulty": problem.difficulty,
        "points": problem.points,
        "constraints": problem.constraints,
        "category": problem.category.name if problem.category else None,
        "tags": [t.name for t in problem.tags.all()],
        "start_function": start_functions,
        "examples": [
            {"id": ex.id, "input_txt": ex.input_txt, "output_txt": ex.output_txt, "explanation": ex.explanation}
            for ex in problem.examples.all()
        ],
        "hints": [{"id": h.id, "text": h.text} for h in problem.hints.all()],
        "challenges": [{"id": c.id, "text": c.text} for c in problem.challenges.all()],
        "videos": videos_data,
        "questions": question_data,
        "is_completed": problem.id in user_completed
    }
