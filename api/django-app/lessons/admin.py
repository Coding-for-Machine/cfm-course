from django.contrib import admin
from .models import Lesson
from unfold.admin import ModelAdmin
from django.utils.text import slugify


class LessonAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Lesson, LessonAdmin)