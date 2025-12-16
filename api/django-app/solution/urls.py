from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    # Submit solution
    path('submit/', views.submit_solution, name='submit'),
    
    # User solutions
    path('', views.get_user_solutions, name='list'),
    path('<int:solution_id>/', views.get_solution_detail, name='detail'),
    
    # Leaderboard
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
]