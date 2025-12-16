from django.contrib import admin
# from django import forms
# from unfold.admin import ModelAdmin
# from .models import Solution


# class SolutionAdminForm(forms.ModelForm):
#     class Meta:
#         model = Solution
#         fields = '__all__'

#     def clean_score(self):
#         score = self.cleaned_data.get('score')
#         if score and score < 0:
#             raise forms.ValidationError("Score cannot be negative.")
#         return score


# @admin.register(Solution)
# class SolutionAdmin(ModelAdmin): 
#     form = SolutionAdminForm

#     list_display = (
#         'user', 'problem', 'language',
#         'is_accepted', 'score',
#         'execution_time', 'memory_usage',
#         'created_at'
#     )
#     search_fields = ('user__email', 'problem__title', 'language__name')
#     list_filter = ('is_accepted', 'language')
#     readonly_fields = ('created_at', 'updated_at', 'score')

#     fieldsets = (
#         (None, {
#             "fields": ("user", "problem", "language"),
#         }),
#         ("Status & Metrics", {
#             "fields": ("is_accepted", "score", "execution_time", "memory_usage"),
#         }),
#         ("Timestamps", {
#             "fields": ("created_at", "updated_at"),
#             "classes": ("collapse",), 
#         }),
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).order_by('-created_at')
