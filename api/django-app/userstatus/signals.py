from django.db.models.signals import post_save
from django.dispatch import receiver
from solution.models import Solution
from .models import UserActivityDaily, UserStats, UserProblemStatus
from django.utils import timezone

@receiver(post_save, sender=Solution)
def solution_created_or_updated(sender, instance, created, **kwargs):
    """
    Bu signal yechim yaratish yoki yangilash vaqtida ishga tushadi.
    - Foydalanuvchining faoliyatini UserActivityDaily'ga yozadi.
    - Agar yechim qabul qilingan bo'lsa, UserProblemStatus orqali muammoni yakunlandi deb belgilaydi.
    - Foydalanuvchining statistikalarini yangilaydi.
    """
    try:
        if created:
            UserActivityDaily.log_activity(
                instance.user,
                activity_type='problem_solved',
                duration=instance.execution_time,  # Bu yerda kerakli bo'lsa vaqtni moslashtirishingiz mumkin yanu web Socket dan foydalansak userni qancha vaqt da problems yechganini bilib olamiz
                score=instance.score
            )
            if instance.is_accepted:
                UserProblemStatus.mark_completed(instance.user, instance.problem)
                UserStats.update_stats(instance.user)

        else:
            if instance.is_accepted:
                UserStats.update_stats(instance.user)
                UserProblemStatus.mark_completed(instance.user, instance.problem)
    except Exception as e:
        print(f"Yechim yaratilganda yoki yangilanganda xatolik yuz berdi: {e}")
