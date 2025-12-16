from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from authentication.decorators import jwt_required
from users.models import MyUser, Profile
from userstatus.models import UserStats, UserActivityDaily, UserBadge
from utils.responses import APIResponse
from utils.cache import cache_response


@require_http_methods(["GET"])
@jwt_required
@cache_response(timeout=300, key_prefix='user_stats')
def get_user_stats(request, user_id=None):
    """User statistikasini olish"""
    try:
        # Agar user_id berilmagan bo'lsa, current user
        if user_id is None:
            user_id = request.user.id
        
        user = MyUser.objects.get(id=user_id)
        stats = UserStats.objects.get(user=user)
        
        data = {
            'user_id': user.id,
            'username': user.username,
            'stats': {
                'total_solved': stats.total_solved,
                'easy_solved': stats.easy_solved,
                'medium_solved': stats.medium_solved,
                'hard_solved': stats.hard_solved,
                'total_score': stats.total_score,
                'current_streak': stats.current_streak,
                'max_streak': stats.max_streak,
                'last_activity': stats.last_activity.isoformat() if stats.last_activity else None,
            }
        }
        
        return APIResponse.success(data)
        
    except MyUser.DoesNotExist:
        return APIResponse.error("User not found", status=404)
    except UserStats.DoesNotExist:
        # Stats mavjud bo'lmasa, yaratish
        UserStats.objects.create(user_id=user_id)
        return get_user_stats(request, user_id)
    except Exception as e:
        return APIResponse.error(str(e), status=500)


@require_http_methods(["GET"])
@jwt_required
def get_profile(request):
    """User profilini olish"""
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        stats = UserStats.objects.get(user=user)
        
        data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'role': user.role,
                'created_at': user.created_at.isoformat(),
            },
            'profile': {
                'bio': profile.bio,
                'age': profile.age,
                'avatar_url': profile.avatar_url,
                'skills': profile.skills,
                'social_links': profile.social_links,
            },
            'stats': {
                'total_solved': stats.total_solved,
                'easy_solved': stats.easy_solved,
                'medium_solved': stats.medium_solved,
                'hard_solved': stats.hard_solved,
                'total_score': stats.total_score,
                'current_streak': stats.current_streak,
                'max_streak': stats.max_streak,
            }
        }
        
        return APIResponse.success(data)
        
    except Exception as e:
        return APIResponse.error(str(e), status=500)