from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Contest, ContestRegistration
from problems.models import Problem

router = Router(tags=["Contests"])


@router.get("/")
def list_contests(request):
    user = request.user if request.user.is_authenticated else None

    contests = (
        Contest.objects.prefetch_related("registrations")
        .filter(is_active=True)
        .order_by("-start_time")
    )

    data = []
    for c in contests:
        if c.has_ended:
            status = "tugadi"
        elif c.is_running:
            status = "faol"
        elif not c.has_started:
            status = "boshlanmadi"
        else:
            status = "noma'lum"

        participated = (
            c.registrations.filter(user=user, is_participated=True).exists()
            if user else False
        )

        data.append({
            "id": c.id,
            "slug": c.slug,
            "title": c.title,
            "start_time": c.start_time.isoformat(),
            "contest_type": c.contest_type,
            "duration": c.duration,
            "participants": c.registrations.count(),
            "description": str(c.description or ""),
            "status": status,
            "participated": participated,
        })

    return {"success": True, "data": data}


@router.post("/{slug}/register/")
def register_contest(request, slug: str, contest_key: str = None):
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "message": "Foydalanuvchi tizimga kirmagan"}

    contest = get_object_or_404(Contest, slug=slug)

    if contest.contest_type == "yopiq":
        if not contest_key:
            return {"success": False, "message": "Bu contest yopiq, iltimos kalitni kiriting"}
        if contest_key != contest.contest_key:
            return {"success": False, "message": "Noto‘g‘ri kalit"}

    registration, created = ContestRegistration.objects.get_or_create(
        user=user,
        contest=contest,
        defaults={"is_participated": True}
    )

    if not created:
        return {"success": False, "message": "Siz allaqachon ro'yxatdan o'tgansiz"}

    return {"success": True, "message": f"Siz '{contest.title}' contestiga muvaffaqiyatli yozildingiz"}


@router.get("/{slug}/")
def contest_detail(request, slug: str):
    user = request.user if request.user.is_authenticated else None
    contest = get_object_or_404(Contest.objects.prefetch_related("registrations"), slug=slug)

    participated = (
        contest.registrations.filter(user=user, is_participated=True).exists()
        if user else False
    )

    if not participated:
        return {"success": False, "message": "Siz contestga yozilmagansiz!"}

    # 🧩 Muammolar (problems)
    problems_data = [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "ball": p.points,
            "type": p.difficulty,
        }
        for p in Problem.objects.filter(contest=contest, is_active=True)
    ]

    # 📋 Status aniqlash
    if contest.has_ended:
        status = "tugadi"
    elif contest.is_running:
        status = "faol"
    elif not contest.has_started:
        status = "boshlanmadi"
    else:
        status = "noma'lum"

    data = {
        "id": contest.id,
        "slug": contest.slug,
        "title": contest.title,
        "description": str(contest.description or ""),
        "start_time": contest.start_time.isoformat(),
        "duration": contest.duration,
        "contest_type": contest.contest_type,
        "participants": contest.registrations.count(),
        "status": status,
        "problems": problems_data,
        "participated": participated,
    }

    return {"success": True, "data": data}
