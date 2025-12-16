from datetime import timedelta
from django.db import models
from django.utils import timezone
from problems.models import Problem
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _

from app.models import TimeMixsin
from users.models import BaseUser as User



class UserActivityDaily(TimeMixsin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField(default=timezone.now)
    activity_count = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0) 
    problem_solved = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date')
        ]
        ordering = ['-date']
        verbose_name = _("User Daily Activity")
        verbose_name_plural = _("User Daily Activities")

    @classmethod
    def log_activity(cls, user, activity_type='problem_solved', duration=0, score=0):
        today = timezone.now().date()
        activity, created = cls.objects.get_or_create(user=user, date=today)
        
        if activity_type == 'problem_solved':
            activity.problem_solved += 1
        activity.activity_count += 1
        activity.total_duration += duration
        activity.score += score
        activity.save()
        return activity


class Badge(TimeMixsin):
    BADGE_TYPES = [
        ('streak', _('Streak')),
        ('solved', _('Problems Solved')),
        ('contest', _('Contest Performance')),
        ('skill', _('Skill Mastery')),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Font awesome icon class
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    threshold = models.IntegerField()  # Minimum requirement to earn
    color = models.CharField(max_length=20, default='#6366f1')  # Badge color

    class Meta:
        verbose_name = _("User Badge")
        verbose_name_plural = _("User Badge")


    def __str__(self):
        return self.name

class UserBadge(TimeMixsin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=100)  # 100% if fully earned

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'badge'], name='unique_user_badge')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.badge.name}"

class UserProblemStatus(TimeMixsin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_status_user')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_status')
    date_completed = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)  
    score = models.PositiveIntegerField(default=0)  

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'problem'], name='unique_user_problem')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.problem.title}"

    @classmethod
    def mark_completed(cls, user, problem):
        points = {
            1: 100,
            2: 250,
            3: 450,
            4: 700
        }.get(problem.difficulty, 100)
        obj, created = cls.objects.update_or_create(
            user=user,
            problem=problem,
            defaults={
                'is_completed': True,
                'score': points,
                'date_completed': timezone.now()  # <-- Yangi qator
            }
        )
        return obj
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_solved = models.PositiveIntegerField(default=0)
    easy_solved = models.PositiveIntegerField(default=0)
    medium_solved = models.PositiveIntegerField(default=0)
    hard_solved = models.PositiveIntegerField(default=0)
    very_hard_solved = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    max_streak = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)

    @classmethod
    def update_stats(cls, user):
        solved_status = user.problem_status_user.filter(is_completed=True)
        
        stats = cls.objects.get_or_create(user=user)[0]
        stats.total_solved = solved_status.count()
        stats.easy_solved = solved_status.filter(problem__difficulty=1).count()
        stats.medium_solved = solved_status.filter(problem__difficulty=2).count()
        stats.hard_solved = solved_status.filter(problem__difficulty=3).count()
        stats.very_hard_solved = solved_status.filter(problem__difficulty=4).count()
        
        stats.total_score = solved_status.aggregate(Sum('score'))['score__sum'] or 0
        
        cls.update_streaks(user, stats)

        last_completed = solved_status.order_by('-date_completed').first()
        if last_completed:
            stats.last_activity = last_completed.date_completed
        
        stats.save()

    @classmethod
    def update_streaks(cls, user, stats):
        streak_count = 0
        max_streak = 0
        prev_date = None
        
        for status in user.problem_status_user.filter(
            is_completed=True
        ).order_by('date_completed'):
            current_date = status.date_completed.date()
            if prev_date and (current_date - prev_date).days == 1:
                streak_count += 1
            else:
                streak_count = 1
            max_streak = max(max_streak, streak_count)
            prev_date = current_date
        
        stats.current_streak = streak_count
        stats.max_streak = max_streak
