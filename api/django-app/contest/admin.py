from django.contrib import admin
from unfold.admin import ModelAdmin
from django import forms
from .models import Contest, UserContestStats, ContestRegistration
from unfold.decorators import display
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget

class MyModelAdminForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = '__all__'
        widgets = {
            'content': AdminMartorWidget,  # TextField nomi
        }

class ContestAdmin(ModelAdmin):
    form = MyModelAdminForm
admin.site.register(Contest, ContestAdmin)


@admin.register(ContestRegistration)
class ContestReagister(ModelAdmin):
    pass


    
@admin.register(UserContestStats)
class UserContestStatsAdmin(ModelAdmin):
    list_display = ('user', 'total_contests', 'display_best_rank', 'average_rank', 'total_points', 'last_contest')
    list_filter = ('total_contests', 'total_points')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'total_contests', 'best_rank', 'average_rank', 'total_points')
    
    @display(description='Eng yaxshi o\'rin', ordering='best_rank')
    def display_best_rank(self, obj):
        if obj.best_rank:
            medal = '🥇' if obj.best_rank == 1 else '🥈' if obj.best_rank == 2 else '🥉' if obj.best_rank == 3 else '🏆'
            return format_html(
                '<span style="background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold;">{} {}</span>',
                medal, obj.best_rank
            )
        return '-'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
