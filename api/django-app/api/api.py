# ==================== api/main.py ====================
from django.conf import settings
from ninja import NinjaAPI
from ninja.errors import HttpError
from django.http import JsonResponse

# API routerlarni import qilish
# from api.auth import router as auth_router
from problems.api import router as problems_router
# from api.solutions import router as solutions_router
from contest.api import router as contests_router
from courses.api import router as courses_router
from quizs.api import router as question_api
# from api.stats import router as stats_router
# API yaratish
api = NinjaAPI(
    title="CodeAlgo Platform API",
    version="1.0.0",
    description="Dasturlash masalalar platformasi uchun REST API",
    docs_url="/docs",
)

# Exception handler
@api.exception_handler(HttpError)
def http_error_handler(request, exc):
    return JsonResponse(
        {
            "error": exc.message,
            "status_code": exc.status_code
        },
        status=exc.status_code
    )

@api.exception_handler(Exception)
def general_exception_handler(request, exc):
    return JsonResponse(
        {
            "error": "Ichki server xatoligi",
            "detail": str(exc) if settings.DEBUG else None
        },
        status=500
    )

# Routerlarni qo'shish
# api.add_router("/auth", auth_router)
api.add_router("/problems", problems_router)
# api.add_router("/solutions", solutions_router)
api.add_router("/contests", contests_router)
api.add_router("/courses", courses_router)
api.add_router("/quiz", question_api)

# Health check endpoint
@api.get("/health")
def health_check(request):
    """API health check"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }