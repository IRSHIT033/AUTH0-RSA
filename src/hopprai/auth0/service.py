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

    return response.json()

