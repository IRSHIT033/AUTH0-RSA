
import requests
from hopprai.core.config import settings


# Function to get the Auth0 management token
def get_auth0_management_token():  
    response = requests.post(
        f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/oauth/token",
        data={"client_id": settings.AUTH0_MANAGEMENT_CLIENT_ID, "client_secret": settings.AUTH0_MANAGEMENT_CLIENT_SECRET, "audience": f"https://{settings.AUTH0_MANAGEMENT_DOMAIN}/api/v2/", "grant_type": "client_credentials"},
    )

    return response.json()["access_token"]
