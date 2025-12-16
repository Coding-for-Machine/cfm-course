from django.contrib import admin
from .models import Course, Enrollment, Modules
from django.utils.text import slugify
from unfold.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget
# Course Admin
class CourseAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'price', 'lesson_count', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)

        super().save_model(request, obj, form, change)  # Avval kursni saqlaymiz

        # Modullarni va darslarni hisoblash
        obj.lesson_count = sum(module.lesson.count() for module in obj.modules.all())
        
        super().save_model(request, obj, form, change)  # Yana saqlaymiz, lesson_count yangilanishi uchun
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
admin.site.register(Course, CourseAdmin)


# Enrollment Admin
class EnrollmentAdmin(ModelAdmin):
    list_display = ('user', 'course', 'is_paid', 'created_at', 'updated_at')
    search_fields = ('user__email', 'course__title')
    list_filter = ('is_paid',)

admin.site.register(Enrollment, EnrollmentAdmin)


# Module Admin
class ModuleAdmin(ModelAdmin):
    list_display = ('title', 'course', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title', 'slug')
    list_filter = ('course',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """
        Modulni saqlashdan oldin slugni sozlash.
        """
        if not obj.slug:
            obj.slug = slugify(obj.title)
        
        super().save_model(request, obj, form, change)  # Avval modulni saqlaymiz

admin.site.register(Modules, ModuleAdmin)