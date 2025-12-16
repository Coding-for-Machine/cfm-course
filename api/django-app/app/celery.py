import os
from celery import Celery

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Django settings bilan integratsiya
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha app’larda tasks.py fayllarni avtomatik topadi
app.autodiscover_tasks()


# Celery konfiguratsiyasi
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Tashkent',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 daqiqa
    task_soft_time_limit=25 * 60,  # 25 daqiqa
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')