# ==================== api/utils/rate_limiter.py ====================
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from ninja.errors import HttpError
from typing import Callable
import hashlib


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_rate(rate_string: str) -> tuple:
    """
    Rate string ni parse qilish
    Masalan: '5/5m' -> (5, 300) # 5 requests in 300 seconds
    """
    count, period = rate_string.split('/')
    count = int(count)
    
    period_map = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
    }
    
    unit = period[-1]
    value = int(period[:-1])
    seconds = value * period_map.get(unit, 60)
    
    return count, seconds


def rate_limit(rate: str, key_func: Callable = None):
    """
    Rate limiting decorator
    
    Args:
        rate: '5/5m' format (5 requests per 5 minutes)
        key_func: Custom key generation function
    
    Usage:
        @rate_limit('10/1m')
        def my_view(request):
            ...
    """
    max_requests, window = parse_rate(rate)
    
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Cache key yaratish
            if key_func:
                cache_key = key_func(request)
            else:
                if hasattr(request, 'user') and request.user.is_authenticated:
                    identifier = f"user_{request.user.id}"
                else:
                    identifier = f"ip_{get_client_ip(request)}"
                
                # Funksiya nomi bilan birga
                func_name = f"{func.__module__}.{func.__name__}"
                cache_key = f"rate_limit:{func_name}:{identifier}"
            
            # Redis dan hozirgi so'rovlar sonini olish
            current = cache.get(cache_key, 0)
            
            if current >= max_requests:
                # TTL ni olish
                ttl = cache.ttl(cache_key)
                raise HttpError(
                    429,
                    f"So'rovlar limiti oshib ketdi. {ttl} soniyadan keyin qayta urinib ko'ring."
                )
            
            # So'rovlar sonini oshirish
            if current == 0:
                cache.set(cache_key, 1, window)
            else:
                cache.incr(cache_key)
            
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator


class RateLimiter:
    """
    Class-based rate limiter
    
    Usage:
        limiter = RateLimiter('10/1m')
        if not limiter.is_allowed(request):
            raise HttpError(429, "Too many requests")
    """
    
    def __init__(self, rate: str):
        self.max_requests, self.window = parse_rate(rate)
    
    def get_cache_key(self, request, prefix: str = 'rate_limit') -> str:
        """Cache key yaratish"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            identifier = f"user_{request.user.id}"
        else:
            identifier = f"ip_{get_client_ip(request)}"
        
        return f"{prefix}:{identifier}"
    
    def is_allowed(self, request, custom_key: str = None) -> tuple[bool, int]:
        """
        Rate limit tekshirish
        
        Returns:
            (is_allowed, remaining_requests)
        """
        cache_key = custom_key or self.get_cache_key(request)
        current = cache.get(cache_key, 0)
        
        if current >= self.max_requests:
            return False, 0
        
        if current == 0:
            cache.set(cache_key, 1, self.window)
        else:
            cache.incr(cache_key)
        
        remaining = self.max_requests - (current + 1)
        return True, remaining
    
    def get_wait_time(self, request, custom_key: str = None) -> int:
        """Kutish vaqtini olish (soniyalarda)"""
        cache_key = custom_key or self.get_cache_key(request)
        return cache.ttl(cache_key) or 0


# ==================== IP based rate limiting ====================
def rate_limit_by_ip(rate: str):
    """Faqat IP manzil bo'yicha rate limiting"""
    max_requests, window = parse_rate(rate)
    
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            ip = get_client_ip(request)
            func_name = f"{func.__module__}.{func.__name__}"
            cache_key = f"rate_limit:ip:{func_name}:{ip}"
            
            current = cache.get(cache_key, 0)
            
            if current >= max_requests:
                ttl = cache.ttl(cache_key)
                raise HttpError(
                    429,
                    f"IP manzil uchun so'rovlar limiti oshdi. {ttl}s kutib turing."
                )
            
            if current == 0:
                cache.set(cache_key, 1, window)
            else:
                cache.incr(cache_key)
            
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator


# ==================== User based rate limiting ====================
def rate_limit_by_user(rate: str):
    """Faqat foydalanuvchi ID bo'yicha rate limiting"""
    max_requests, window = parse_rate(rate)
    
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                raise HttpError(401, "Authentication required")
            
            user_id = request.user.id
            func_name = f"{func.__module__}.{func.__name__}"
            cache_key = f"rate_limit:user:{func_name}:{user_id}"
            
            current = cache.get(cache_key, 0)
            
            if current >= max_requests:
                ttl = cache.ttl(cache_key)
                raise HttpError(
                    429,
                    f"Foydalanuvchi limiti oshdi. {ttl}s kutib turing."
                )
            
            if current == 0:
                cache.set(cache_key, 1, window)
            else:
                cache.incr(cache_key)
            
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator