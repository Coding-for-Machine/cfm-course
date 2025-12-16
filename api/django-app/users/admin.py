from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import MyUser, BaseUser
from django.contrib.admin.models import LogEntry


@admin.register(BaseUser)
class BaseUserAdmin(ModelAdmin):
    list_display = ["username", "telegram_id", "phone", "full_name", "last_login"]

@admin.register(LogEntry)
class LogEntryAdmin(ModelAdmin):
    list_display = (
        'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message'
    )
    list_filter = ('action_time', 'user', 'action_flag')
    readonly_fields = ('action_time', 'user', 'content_type', 'object_repr', 'change_message')

# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
