from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import get_language_info

UNFOLD = {
    "SITE_TITLE": "Coding-for-Machine | Admin",
    "SITE_HEADER": "Coding-for-Machine",
    "SITE_SUBHEADER": "Dasturlash masalalarini hal qilish platformasi",
    "MENU": [
        {
            "label": "👤 Users",
            "icon": "user",
            "items": [
                {"model": "users.myuser", "icon": "user"},
                {"model": "users.profile", "icon": "user-check"},
                {"model": "userstatus.useractivitydaily", "icon": "activity"},
                {"model": "userstatus.userstats", "icon": "bar-chart"},
                {"model": "userstatus.userbadges", "icon": "award"},
                {"model": "userstatus.userproblemstatus", "icon": "check-circle"},
            ]
        },
        {
            "label": "📚 Courses",
            "icon": "book",
            "items": [
                {"model": "courses.course", "icon": "book-open"},
                {"model": "courses.mymodules", "icon": "layers"},
                {"model": "lessons.lesson", "icon": "list"},
                {"model": "problems.category", "icon": "tag"},
                {"model": "problems.language", "icon": "globe"},
            ]
        },
        {
            "label": "🧠 Quizzes",
            "icon": "help-circle",
            "items": [
                {"model": "quizs.quiz", "icon": "file-text"},
                {"model": "quizs.question", "icon": "help-circle"},
                {"model": "quizs.answer", "icon": "edit"},
                {"model": "quizs.quizattempt", "icon": "clock"},
            ]
        },
        {
            "label": "🏆 Contests",
            "icon": "flag",
            "items": [
                {"model": "contest.contest", "icon": "flag"},
                {"model": "contest.contestregistration", "icon": "user-plus"},
                {"model": "contest.userconteststats", "icon": "bar-chart-2"},
            ]
        },
        {
            "label": "💻 Problems",
            "icon": "code",
            "items": [
                {"model": "problems.problem", "icon": "code"},
                {"model": "problems.examples", "icon": "file"},
                {"model": "problems.function", "icon": "cpu"},
                {"model": "problems.executiontestcase", "icon": "play"},
                {"model": "problems.testcase", "icon": "check"},
                {"model": "solution.solution", "icon": "lightbulb"},
            ]
        },
    ],
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("favicon.ico"),
    "SITE_LOGO": lambda request: static("admin/images/leetcode-logo.svg"),
    "SITE_DROPDOWN": [
        {
            "icon": "home",
            "title": _("Saytga o'tish"),
            "link": "/",
        },
        {
            "icon": "code",
            "title": _("LeetCode Problems"),
            "link": "/problems/",
        },
        {
            "icon": "trophy",
            "title": _("Olimpiada"),
            "link": "/contest/",
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "THEME": None,
    "LOGIN": {
        "image": lambda request: static("admin/login-bg.jpg"),
    },
    "SHOW_LANGUAGES": True,
    "LANGUAGES": {
        "navigation": [
            {
                'bidi': False,
                'code': 'en',
                'name': 'English',
                'name_local': get_language_info('en')['name_local'],
                'name_translated': _('English')
            },
            {
                'bidi': False,
                'code': 'uz',
                'name': 'Uzbek',
                'name_local': get_language_info('uz')['name_local'],
                'name_translated': _('Uzbek')
            },
            {
                'bidi': False,
                'code': 'ru',
                'name': 'Russian',
                'name_local': get_language_info('ru')['name_local'],
                'name_translated': _('Russian')
            },
        ]
    },
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "primary": {
            "50": "239, 246, 255",
            "100": "219, 234, 254",
            "200": "191, 219, 254",
            "300": "147, 197, 253",
            "400": "96, 165, 250",
            "500": "59, 130, 246",
            "600": "37, 99, 235",
            "700": "29, 78, 216",
            "800": "30, 64, 175",
            "900": "30, 58, 138",
            "950": "23, 37, 84",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation_expanded": True,
    },
    # "DASHBOARD_CALLBACK": "app.admin_dashboard.dashboard_callback",
}

def get_unfoldadmin_settings():
    return UNFOLD