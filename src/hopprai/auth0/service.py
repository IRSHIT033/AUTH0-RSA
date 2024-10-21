from fastapi import HTTPException
import requests
from .token import get_auth0_management_token
from hopprai.core.config import settings


def get_user_roles_inside_org(user_id: str, org_id: str):
    management_token = get_auth0_management_token()

    # Get the user roles inside the organization using the management api
    response = requests.get(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/members/{user_id}/roles",
        headers={"Authorization": f"Bearer {management_token}"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

def get_users_of_org(org_id: str,per_page:int=100,page:int=0):
    management_token = get_auth0_management_token()

    response = requests.get(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/members",
        headers={"Authorization": f"Bearer {management_token}"},
        params={"per_page_user": per_page, "page": page}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

def invite_user_to_org(inviter_name:str, invitee_email: str, org_id: str):
    management_token = get_auth0_management_token()

    # Invite the user to the organization using the management api
    response = requests.post(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/invitations",
        headers={"Authorization": f"Bearer {management_token}"},
        json={
            "inviter": {
                "name": inviter_name,
            },
            "invitee": {
                "email": invitee_email,
            },
           "client_id": settings.AUTH0_CLIENT_ID,
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


def add_roles_to_user(user_id: str, org_id: str, roles_to_assign: list[str]):
    management_token = get_auth0_management_token()
    
    # Add roles to the user inside the organization using the management api
    response = requests.post(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/members/{user_id}/roles",
        headers={"Authorization": f"Bearer {management_token}"},
        json={"roles": roles_to_assign}
    )
    
    if response.status_code != 204:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

def remove_roles_from_user(user_id: str, org_id: str, roles_to_remove: list[str]):
    management_token = get_auth0_management_token()

    response = requests.delete(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/members/{user_id}/roles",
        headers={"Authorization": f"Bearer {management_token}"},
        json={"roles": roles_to_remove}
    )

    if response.status_code != 204:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


def remove_user_from_org(user_id: str, org_id: str):
    management_token = get_auth0_management_token()

    # Remove the user from the organization using the management api
    response = requests.delete(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/organizations/{org_id}/members",
        headers={"Authorization": f"Bearer {management_token}"},
        json={"members": [user_id]}
    )

    if response.status_code != 204:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
