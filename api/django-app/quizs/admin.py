from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline  
from lessons.models import Lesson
from .models import Quiz, Question, Answer, QuizAttempt


@admin.register(QuizAttempt)
class QuizAttemptAdmin(ModelAdmin):
    list_display = ("id", "user", "quiz", "score", "completed_at")
    list_filter = ("quiz", "completed_at")
    search_fields = ("user__username", "quiz__title")


class AnswerInline(TabularInline):  
    model = Answer
    extra = 1 
    min_num = 1
    fields = ('description', 'is_correct')


@admin.register(Quiz)
class QuizAdmin(ModelAdmin):  
    list_display = ('title', 'slug', 'time_limit', 'created_at')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)} 
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Question)
class QuestionAdmin(ModelAdmin):  
    list_display = ('description', 'created_at')
    search_fields = ('description',)
    ordering = ('-created_at',)
    inlines = [AnswerInline] 


@admin.register(Answer)
class AnswerAdmin(ModelAdmin): 
    list_display = ('description', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('description',)
