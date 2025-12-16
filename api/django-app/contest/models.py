# ==================== contest/models.py ====================
from datetime import timedelta
from django.db import models
from django.utils import timezone
from martor.models import MartorField
from users.models import BaseUser as User

class Contest(models.Model):
    CONTEST_TYPE_CHOICES = [
        ('yopiq', 'Yopiq'),
        ('ochiq', 'Ochiq'),
    ]
    
    title = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(max_length=200, verbose_name="slug")
    contest_type = models.CharField(max_length=20, choices=CONTEST_TYPE_CHOICES, verbose_name="Turi")
    contest_key = models.PositiveIntegerField(blank=True, null=True, help_text="Tanlov Kaliti", verbose_name="Kalit")
    start_time = models.DateTimeField(verbose_name="Boshlanish vaqti")
    duration = models.PositiveIntegerField(help_text="Daqiqalarda", verbose_name="Davomiyligi")
    description = MartorField(blank=True, null=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = "Contest"
        verbose_name_plural = "Contestlar"
    
    def __str__(self):
        return f"{self.title} (#{self.id})"

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)
    
    @property
    def has_started(self):
        return timezone.now() >= self.start_time
    
    @property
    def has_ended(self):
        return timezone.now() >= self.end_time
    
    @property
    def is_running(self):
        return self.has_started and not self.has_ended

    # ✅ Helper method: qat’iy filterlar uchun
    @classmethod
    def running_contests(cls):
        now = timezone.now()
        return cls.objects.filter(start_time__lte=now, start_time__gte=now - models.F('duration')*60)

class ContestRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contest_registrations")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan")
    is_participated = models.BooleanField(default=False, verbose_name="Ishtirok etdi")
    
    class Meta:
        unique_together = ('user', 'contest')
        verbose_name = "Contest Ro'yxati"
        verbose_name_plural = "Contest Ro'yxatlari"
    
    def __str__(self):
        return f"{self.user.id} - {self.contest.title}"

    # ✅ Helper method: qat’iy qatnashgan foydalanuvchilar
    @classmethod
    def active_users(cls, contest):
        return cls.objects.filter(contest=contest, is_participated=True).select_related('user')


class UserContestStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='contest_stats')
    total_contests = models.PositiveIntegerField(default=0)
    best_rank = models.PositiveIntegerField(null=True, blank=True)
    average_rank = models.FloatField(null=True, blank=True)
    total_points = models.PositiveIntegerField(default=0)
    last_contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = "Contest Statistika"
        verbose_name_plural = "Contest Statistikalar"
    
    def __str__(self):
        return f"{self.user.id} statistikasi"

    # ✅ Helper methods for performance
    @property
    def participated_contests_count(self):
        return self.user.contest_registrations.filter(is_participated=True).count()

    @property
    def running_contests(self):
        now = timezone.now()
        return self.user.contest_registrations.filter(
            contest__start_time__lte=now,
            contest__start_time__gte=now - models.F('contest__duration')*60
        )
