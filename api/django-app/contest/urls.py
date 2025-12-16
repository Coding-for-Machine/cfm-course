from django.urls import path
from contest import views

app_name = 'contest'

urlpatterns = [
    # Contest list & detail
    path('', views.get_contests, name='list'),
    path('<int:contest_id>/', views.get_contest_detail, name='detail'),
    
    # Registration
    path('<int:contest_id>/register/', views.register_contest, name='register'),
    path('<int:contest_id>/unregister/', views.unregister_contest, name='unregister'),
    
    # Rankings
    path('<int:contest_id>/rankings/', views.get_contest_rankings, name='rankings'),
    
    # User contests
    path('my-contests/', views.get_user_contests, name='user_contests'),
]