from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
    path('', views.get_courses, name='list'),
    path('<slug:slug>/', views.get_course_detail, name='detail'),
    
    # Enrollment
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll'),
    
    # Modules & Lessons
    path('<slug:slug>/modules/', views.get_course_modules, name='modules'),
    path('lessons/<slug:lesson_slug>/', views.get_lesson_detail, name='lesson_detail'),
    
    # Quiz
    path('quiz/<slug:quiz_slug>/', views.get_quiz, name='quiz'),
    path('quiz/<slug:quiz_slug>/submit/', views.submit_quiz, name='submit_quiz'),
]