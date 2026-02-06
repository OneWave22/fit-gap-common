import os
from typing import Dict, Any
from urllib.parse import urlencode

import jwt
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"


def build_google_auth_url(state: str) -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    if not client_id or not redirect_uri:
        raise RuntimeError("Google OAuth env missing (GOOGLE_CLIENT_ID/GOOGLE_REDIRECT_URI)")

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    if not client_id or not client_secret or not redirect_uri:
        raise RuntimeError("Google OAuth env missing (client_id/secret/redirect)")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    res = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
    if res.status_code != 200:
        raise RuntimeError(f"Token exchange failed: {res.status_code} {res.text}")
    return res.json()


def verify_google_id_token(id_token: str) -> Dict[str, Any]:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise RuntimeError("Google OAuth env missing (GOOGLE_CLIENT_ID)")

    headers = jwt.get_unverified_header(id_token)
    kid = headers.get("kid")
    if not kid:
        raise ValueError("No kid in token header")

    jwks = requests.get(GOOGLE_JWKS_URL, timeout=10).json()
    key = None
    for jwk in jwks.get("keys", []):
        if jwk.get("kid") == kid:
            key = jwk
            break
    if not key:
        raise ValueError("No matching JWK")

    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
    payload = jwt.decode(
        id_token,
        public_key,
        algorithms=["RS256"],
        audience=client_id,
        issuer=["https://accounts.google.com", "accounts.google.com"],
    )
    return payload
