from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import requests
from hopprai.auth0.dependencies import RoleChecker
from hopprai.auth0.service import get_user_roles_inside_org
from hopprai.core.config import settings
from hopprai.core.util import decode_access_token, decode_id_token


router = APIRouter()


# Endpoint to login via Auth0 (redirects to Auth0 login page)
@router.get("/login")
async def login():
    return RedirectResponse(
        f"https://{settings.AUTH0_DOMAIN}/authorize"
        "?response_type=code"
        f"&client_id={settings.AUTH0_CLIENT_ID}"
        f"&redirect_uri={settings.APPLICATION_URL}/token"
        "&scope=offline_access openid profile email"
        f"&audience={settings.AUTH0_API_AUDIENCE}"
    )


@router.get("/token")
async def get_access_token(code: str):
    payload = (
        "grant_type=authorization_code"
        f"&client_id={settings.AUTH0_CLIENT_ID}"
        f"&client_secret={settings.AUTH0_CLIENT_SECRET}"
        f"&code={code}"
        f"&redirect_uri={settings.APPLICATION_URL}/token"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        f"https://{settings.AUTH0_DOMAIN}/oauth/token",
        data=payload,
        headers=headers,
    )
    return response.json()


@router.get("/roles")
async def get_user_roles(user_id: str, org_id: str):
    return get_user_roles_inside_org(user_id, org_id)

@router.get("/decode-token")
async def decode_token(details: any=Depends(decode_access_token)):
    return details

@router.get("/get-profile")
async def decode_id_token(details: any=Depends(decode_id_token)):
    return details




