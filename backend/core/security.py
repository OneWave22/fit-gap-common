import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer(auto_error=False)


def _get_env(name: str, default: Optional[str] = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Missing env: {name}")
    return val


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _create_token(payload: Dict[str, Any], ttl_seconds: int) -> str:
    secret = _get_env("JWT_SECRET")
    exp = _now_utc() + timedelta(seconds=ttl_seconds)
    data = {**payload, "exp": exp}
    return jwt.encode(data, secret, algorithm="HS256")


def create_access_token(user_id: str, role: Optional[str], ttl_minutes: int) -> str:
    return _create_token(
        {"typ": "access", "sub": user_id, "role": role}, ttl_minutes * 60
    )


def create_refresh_token(user_id: str, ttl_days: int) -> str:
    return _create_token({"typ": "refresh", "sub": user_id}, ttl_days * 24 * 3600)


def create_signup_token(
    provider: str, provider_sub: str, email: Optional[str], ttl_minutes: int
) -> str:
    return _create_token(
        {
            "typ": "signup",
            "provider": provider,
            "sub": provider_sub,
            "email": email,
        },
        ttl_minutes * 60,
    )


def create_state_token(ttl_minutes: int) -> str:
    return _create_token({"typ": "state"}, ttl_minutes * 60)


def decode_token(token: str) -> Dict[str, Any]:
    secret = _get_env("JWT_SECRET")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="TOKEN_EXPIRED")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")


def _get_token(
    auth: Optional[HTTPAuthorizationCredentials],
) -> str:
    if auth and auth.credentials:
        return auth.credentials
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="MISSING_TOKEN")


def require_access_token(
    request: Request,
    auth: Optional[HTTPAuthorizationCredentials] = Security(security),
) -> Dict[str, Any]:
    token = _get_token(auth)
    payload = decode_token(token)
    if payload.get("typ") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN_TYPE")
    return payload


def require_signup_token(
    request: Request,
    auth: Optional[HTTPAuthorizationCredentials] = Security(security),
) -> Dict[str, Any]:
    token = _get_token(auth)
    payload = decode_token(token)
    if payload.get("typ") != "signup":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN_TYPE")
    return payload


def get_cookie_settings() -> Dict[str, Any]:
    return {
        "domain": os.getenv("COOKIE_DOMAIN") or None,
        "secure": os.getenv("COOKIE_SECURE", "false").lower() == "true",
        "samesite": os.getenv("COOKIE_SAMESITE", "lax"),
        "path": "/",
    }
