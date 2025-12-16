# api/utils/auth.py
import jwt
from ninja.security import HttpBearer
from django.http import HttpRequest
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidTokenError
from asgiref.sync import async_to_sync
from datetime import datetime

from users.models import BaseUser
from .auth_service_status import auth_service_verify, auth_service_get_current_user


def verify_jwt(token: str):
    """
    JWT tokenini tekshiradi va payload qaytaradi.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except (ExpiredSignatureError, InvalidTokenError):
        return None


class JWTBearer(HttpBearer):
    """
    Ninja uchun JWT autentifikatsiya sinfi.
    """

    def authenticate(self, request: HttpRequest, token: str):
        payload = verify_jwt(token)
        print(payload, token)  # Debug uchun

        if payload is None:
            return None  # Ninja avtomatik 401

        telegram_id = payload.get("telegram_id")
        username = payload.get("username")
        if not telegram_id and not username:
            return None

        # User bazada mavjudmi tekshirish
        if BaseUser.objects.filter(telegram_id=telegram_id).exists():
            ok, status = async_to_sync(auth_service_verify)(token)
            if ok and status == 200:
                return payload
            return None
        else:
            user_data, status = async_to_sync(auth_service_get_current_user)(token)
            if status == 200 and "user" in user_data:
                u = user_data["user"]

                print("user-data", user_data)
                # last_login formatini tekshirish
                last_login_val = u.get("last_login")
                if last_login_val:
                    try:
                        # YYYY-MM-DD HH:MM:SS format
                        last_login_val = datetime.strptime(last_login_val, "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        try:
                            # timestamp bo'lsa
                            last_login_val = datetime.fromtimestamp(int(last_login_val))
                        except Exception:
                            last_login_val = None
                BaseUser.objects.update_or_create(
                    telegram_id=int(u["user_id"]),
                    defaults={
                        "username": u.get("username"),
                        "phone": u.get("phone"),
                        "full_name": u.get("full_name"),
                        "last_login": last_login_val
                    }
                )
                return payload

        return None
