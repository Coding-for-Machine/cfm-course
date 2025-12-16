from django.db import models
from django.contrib.contenttypes.models import ContentType
from problems.models import Language, Problem
from userstatus.models import UserProblemStatus
from problems.models import TimeMixsin

from users.models import BaseUser as User


class Solution(TimeMixsin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="solution")
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  
    code = models.TextField()
    is_accepted = models.BooleanField(default=False)
    execution_time = models.FloatField(default=0.0)  
    memory_usage = models.FloatField(default=0.0)  
    score = models.PositiveIntegerField(default=0)  
    passed_tests = models.PositiveIntegerField(default=0)  
    total_tests = models.PositiveIntegerField(default=0)  
    testcases_json = models.JSONField()
    """
    Agar kerak bulsa unique_together ni qo'shish kerak.
    Bu ('user', 'problem', 'language') ni unique qiladi yani 1 ta user faqat bitta problem va language uchin 
    bitta natija kirgazish mumkun yani bitta urinish
    """
    # class Meta:
    #     unique_together = ('user', 'problem', 'language')  

    def __str__(self):
        return f"{self.user.email} - {self.problem.title} ({self.language}) - {'Accepted' if self.is_accepted else 'Pending'}"

    @classmethod
    def create(cls, user, problem, language, code, execution_time, memory_usage, passed_tests, total_tests, testcases_json):
        solution = cls.objects.create(
            user=user,
            problem=problem,
            language=language,
            code=code,
            execution_time=execution_time,
            memory_usage=memory_usage,
            passed_tests=passed_tests,
            total_tests=total_tests,
            testcases_json=testcases_json,
            is_accepted=passed_tests == total_tests  
        )
        solution.save()

        if solution.is_accepted:
            UserProblemStatus.mark_completed(user, problem)

        return solution
# import json
# from django.db import models
# from django.utils import timezone
# from django.db.models import Count, Avg, Q, F
# from problems.models import Language, Problem
# from app.models import TimeMixsin
# from django.conf import settings


# User = settings.AUTH_USER_MODEL

# class Solution(TimeMixsin):
#     user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True, 
#         related_name='solution',
#         verbose_name='Foydalanuvchi'
#     )
#     language = models.ForeignKey(
#         Language,
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True, 
#         related_name='solution',
#         verbose_name='Dasturlash tili'
#     )
#     problem = models.ForeignKey(
#         Problem,
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True, 
#         related_name='solution',
#         verbose_name='Dasturlash tili'
#     )
#     code = models.TextField(verbose_name='Kod')
#     execution_time = models.FloatField(default=0.0, verbose_name='Bajarish vaqti (s)')
#     memory_used = models.IntegerField(default=0, verbose_name='Xotira (KB)')
#     test_results = models.JSONField(
#         null=True, 
#         blank=True, 
#         default=dict,
#         verbose_name='Test natijalari'
#     )