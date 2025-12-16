from django.urls import path
from problems import views

app_name = 'problems'

urlpatterns = [
    # Problem list & detail
    path('', views.get_problems, name='list'),
    path('<slug:slug>/', views.get_problem_detail, name='detail'),
    path('<slug:slug>/status/', views.get_user_problem_status, name='status'),
    path('<slug:slug>/starter-code/<slug:language_slug>/', views.get_starter_code, name='starter_code'),
    
    # Categories & Languages
    path('meta/categories/', views.get_categories, name='categories'),
    path('meta/languages/', views.get_languages, name='languages'),
]
