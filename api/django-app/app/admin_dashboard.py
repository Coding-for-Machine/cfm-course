# app/admin_dashboard.py
from django.utils import timezone
from django.db.models import Count, Q
from users.models import MyUser
from problems.models import Problem
from solution.models import Solution
from contest.models import Contest

def dashboard_callback(request, context):
    total_users = MyUser.objects.filter(is_deleted=False).count()
    active_users = MyUser.objects.filter(is_active=True, is_deleted=False).count()
    
    total_problems = Problem.objects.all().count()
    problems_by_difficulty = {
        'easy': Problem.objects.filter(difficulty=1).count(),
        'medium': Problem.objects.filter(difficulty=2).count(),
        'hard': Problem.objects.filter(difficulty=3).count(),
        'very_hard': Problem.objects.filter(difficulty=4).count(),
    }
    
    # Solutions
    total_solutions = Solution.objects.all().count()
    accepted_solutions = Solution.objects.filter(is_accepted=True).count()
    acceptance_rate = (accepted_solutions / total_solutions * 100) if total_solutions > 0 else 0
    
    # Contests
    active_contests = Contest.objects.filter(is_active=True).count()
    
    # Top users
    top_users = MyUser.objects.annotate(
        solved_count=Count('solution', filter=Q(solution__is_accepted=True))
    ).order_by('-solved_count')[:5]
    
    # Recent solutions
    try:
        recent_solutions = Solution.objects.select_related(
            'user', 'problem', 'language'
        ).order_by('-created_at')[:10]
    except:
        recent_solutions = []
    
    # context.update({
    #     'total_users': total_users,
    #     'active_users': active_users,
    #     'total_problems': total_problems,
    #     'problems_by_difficulty': problems_by_difficulty,
    #     'total_solutions': total_solutions,
    #     'accepted_solutions': accepted_solutions,
    #     'acceptance_rate': round(acceptance_rate, 1),
    #     'active_contests': active_contests,
    #     'top_users': top_users,
    #     'recent_solutions': recent_solutions,
    # })
    
    return context