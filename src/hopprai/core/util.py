
from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from hopprai.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_jwks():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def decode_token(token: str, audience: str, issuer: str):
    try:
        jwks = get_jwks()  # Reuse your existing function to get JWKS
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=audience,  # Use dynamic audience
                issuer=issuer  # Use dynamic issuer
            )
            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find the appropriate key"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid"
        )


def decode_access_token(token: str = Depends(oauth2_scheme)):
    return decode_token(
        token=token,
        audience=settings.AUTH0_API_AUDIENCE,  # API Audience for access tokens
        issuer=f"https://{settings.AUTH0_DOMAIN}/"  # Auth0 domain as issuer
    )

def decode_id_token(token: str=Depends(oauth2_scheme)):
    return decode_token(
        token=token,
        audience=settings.AUTH0_CLIENT_ID,  # Client ID for ID tokens
        issuer=f"https://{settings.AUTH0_DOMAIN}/"  # Auth0 domain as issuer
    )