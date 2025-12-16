from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import (
    UserActivityDaily, Badge, UserBadge, 
    UserProblemStatus
)

@admin.register(UserActivityDaily)
class UserActivityDailyAdmin(ModelAdmin):
    list_display = ('user', 'date', 'activity_count', 'formatted_duration', 'score')
    list_filter = ('date',)
    search_fields = ('user__email',)
    ordering = ('-date',)
    readonly_fields = ('date',)

    def formatted_duration(self, obj):
        minutes = obj.total_duration // 60
        seconds = obj.total_duration % 60
        return f"{minutes}m {seconds}s"
    formatted_duration.short_description = "Total Duration"


@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    list_display = ('name', 'description', 'icon_preview')
    search_fields = ('name',)
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />',
                obj.icon.url
            )
        return format_html('<span style="color: gray;">No Icon</span>')
    icon_preview.short_description = "Icon"


@admin.register(UserBadge)
class UserBadgeAdmin(ModelAdmin):
    list_display = ('user', 'badge', 'date_earned', 'badge_icon')
    list_filter = ('badge', 'date_earned')
    search_fields = ('user__email', 'badge__name')
    readonly_fields = ('date_earned',)

    def badge_icon(self, obj):
        if obj.badge and obj.badge.icon:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" title="{}" />',
                obj.badge.icon.url,
                obj.badge.name
            )
        return "-"
    badge_icon.short_description = "Badge"


@admin.register(UserProblemStatus)
class UserProblemStatusAdmin(ModelAdmin):
    list_display = ('user', 'problem', 'is_completed_icon', 'score')
    list_filter = ('is_completed',)
    search_fields = ('user__email', 'problem__title')
    ordering = ('-score',)

    def is_completed_icon(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green;">Yechilgan</span>')
        return format_html('<span style="color:red;">Yechilmagan</span>')
    is_completed_icon.short_description = "Completed"
