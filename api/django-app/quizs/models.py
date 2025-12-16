from django.db import models
from app.models import TimeMixsin
from utils.get_slug import generate_slug_with_case
from problems.models import Problem
from courses.models import Modules
from martor.models import MartorField

from users.models import BaseUser as User


class Quiz(TimeMixsin):
    module = models.ForeignKey(Modules, on_delete=models.SET_NULL, null=True, blank=True) 
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = MartorField()
    time_limit = models.PositiveIntegerField(default=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passing_score = models.PositiveIntegerField(default=70)
    show_correct_answers = models.BooleanField(default=True)
    attempts_allowed = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(self.title)
        super().save(*args, **kwargs)

class Question(TimeMixsin):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, blank=True, null=True, related_name='questions')
    problems = models.ForeignKey(Problem, on_delete=models.SET_NULL, blank=True, null=True)
    description = MartorField()
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"
    def __str__(self):
        return f"Savol-> {self.description[:50]}"


class Answer(TimeMixsin):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    description = MartorField()
    is_correct = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variyatlar" 

    def __str__(self):
        return f"{self.pk}--{self.description}"
    

class QuestionAttempt(TimeMixsin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question Attempt"
        verbose_name_plural = "Question Attempts"
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user} - {self.question}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)
    details = models.JSONField(default=dict)  # {question_id: {'answer_id': 1, 'correct': True}}

    class Meta:
        ordering = ['-completed_at']
        unique_together = ['user', 'quiz', 'started_at']

    def duration(self):
        return (self.completed_at - self.started_at).total_seconds()
