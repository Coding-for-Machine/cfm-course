import httpx
from decouple import config
from typing import Tuple, Optional, Dict

AUTH_SERVER_BASE_URL = config("AUTH_SERVER_BASE_URL")


async def auth_service_verify(token: str) -> Tuple[bool, Optional[int]]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{AUTH_SERVER_BASE_URL}/api/verify", headers=headers)
            resp.raise_for_status()
            return True, resp.status_code
        except httpx.HTTPStatusError as e:
            return False, e.response.status_code if e.response else None
        except httpx.RequestError:
            return False, None


async def auth_service_get_current_user(token: str) -> Tuple[Dict, Optional[int]]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(f"{AUTH_SERVER_BASE_URL}/api/user", headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except httpx.HTTPStatusError as e:
            return {"error": f"Auth failed: {e.response.status_code}"}, e.response.status_code if e.response else None
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}, None
