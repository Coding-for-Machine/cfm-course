# ==================== api/utils/auth.py ====================
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from typing import Optional

User = get_user_model()


class JWTAuth(HttpBearer):
    
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user_id = payload.get('user_id')
            if not user_id:
                return None
            
            user = User.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return None
            
            # Token blacklist tekshirish
            from users.models import BlockedToken
            if BlockedToken.objects.filter(token=token).exists():
                return None
            
            request.user = user
            return user
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None


def create_access_token(user_id: int, **extra_payload) -> str:
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME),
        'iat': datetime.utcnow(),
        **extra_payload
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int, **extra_payload) -> str:
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME),
        'iat': datetime.utcnow(),
        **extra_payload
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token muddati tugagan")
    except jwt.InvalidTokenError:
        raise ValueError("Noto'g'ri token")


def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = verify_token(refresh_token)
        
        if payload.get('type') != 'refresh':
            raise ValueError("Bu refresh token emas")
        
        user_id = payload.get('user_id')
        return create_access_token(user_id)
    except Exception as e:
        raise ValueError(f"Token yangilanmadi: {str(e)}")