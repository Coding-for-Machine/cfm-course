import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key

from .admin_site import get_unfoldadmin_settings
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY', default='a-string-secret-at-least-256-bits-long')
DEBUG = config('DEBUG', default=True, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
ALLOWED_HOSTS = ['*']  
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "http://0.0.0.0:8000",
]



INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "import_export",
    # -----------------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed package
    "corsheaders",
    'storages',
    'django_celery_results',
    'django_celery_beat',
    'martor',

    # myapp
    'problems.apps.ProblemsConfig',
    'users',
    'solution.apps.SolutionConfig',
    'userstatus.apps.UserstatusConfig',
    'contest.apps.ContestConfig',
    'courses.apps.CoursesConfig',
    'quizs.apps.QuizsConfig',
    'lessons',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # add
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'users.middleware.CookieJWTAuth',  # Sizning maxsus middleware
]

# Hammaga ruxsat berish (faqat ishlab chiqish uchun)
CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'POST',
    'PUT',
]



CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]



ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database configuration - Corrected version
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "mydb",
#         "USER": "mydb",
#         "PASSWORD": "mydb",
#         "HOST": "db",  # docker-compose service nomi
#         "PORT": "5433",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', 'mydb'),
        'USER': config('DB_USER', 'myuser'),
        'PASSWORD': config('DB_PASSWORD', 'mypassword'),
        'HOST': config('DB_HOST', 'localhost'),  # localhost
        'PORT': config('DB_PORT', '5433'),       # host port
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# REDIS CACHE
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'PICKLE_VERSION': -1,
        },
        'KEY_PREFIX': 'leetcode',
        'TIMEOUT': 300,
    }
}

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ==========================================
# CELERY CONFIGURATION
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tashkent'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
CELERY_WORKER_PREFETCH_MULTIPLIER = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000


# UNFOLD settings
UNFOLD = get_unfoldadmin_settings()

# users-foydalanovchi
AUTH_USER_MODEL = "users.MyUser"


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -----------------------------------------stroge----------------------------------
# MinIO yoki AWS S3 Hozircha MinIO dan foydalanamiz
# ==========================================
# AWS / MinIO
# ==========================================
AWS_ACCESS_KEY_ID = config('MINIO_ACCESS_KEY', default='minioadmin')
AWS_SECRET_ACCESS_KEY = config('MINIO_SECRET_KEY', default='minioadmin123')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_ENDPOINT_URL = config('MINIO_ENDPOINT', default='http://localhost:9000')
AWS_S3_USE_SSL = config("AWS_S3_USE_SSL", cast=bool, default=False)
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = config("MINIO_PUBLIC_DOMAIN")

AWS_STORAGE_BUCKET_NAME = 'media'


STORAGES = {
    "default": {
        "BACKEND": "app.storages.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "app.storages.StaticStorage",
    },
}

# ==========================================
# STATIC FILES
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'app.storages.StaticStorage'

# ==========================================
# MEDIA FILES
# ==========================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'
DEFAULT_FILE_STORAGE = 'app.storages.MediaStorage'
# ==========================================
# VIDEO PROCESSING
# ==========================================
VIDEO_UPLOAD_PATH = 'videos/originals/'
VIDEO_HLS_PATH = 'videos/hls/'
VIDEO_THUMBNAILS_PATH = 'videos/thumbnails/'

FFMPEG_PATH = config('FFMPEG_PATH', default='/usr/bin/ffmpeg')
FFPROBE_PATH = config('FFPROBE_PATH', default='/usr/bin/ffprobe')

VIDEO_QUALITIES = [
    {'name': '360p', 'width': 640, 'height': 360, 'bitrate': '800k'},
    {'name': '480p', 'width': 854, 'height': 480, 'bitrate': '1400k'},
    {'name': '720p', 'width': 1280, 'height': 720, 'bitrate': '2800k'},
    {'name': '1080p', 'width': 1920, 'height': 1080, 'bitrate': '5000k'},
]

# ==========================================
# AUTH
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================
# INTERNATIONALIZATION
# ==========================================
LANGUAGE_CODE = 'uz-uz'
LANGUAGES = [
    ('uz', 'Oʻzbekcha'),
    ('ru', 'Русский'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# ==========================================
# SECURITY (Production)
# ==========================================
if not DEBUG:
    # SECURE_SSL_REDIRECT = True
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # X_FRAME_OPTIONS = 'DENY'
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    pass

# ==========================================
# LOGGING
# ==========================================
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Keyin LOGGING konfiguratsiyasida:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'django.log'),  # str() qo'shing
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# MARTOR (Markdown Editor)
# ==========================================
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',
    'imgur': 'false',
    'mention': 'false',
    'jquery': 'true',
    'living': 'false',
    'spellcheck': 'false',
    'hljs': 'true',
}

MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
]
