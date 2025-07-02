from pathlib import Path
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.dto.response.error.http_error_response import HttpUnauthorizationResponse


security = HTTPBearer()

# Path to your public key
PUBLIC_KEY_PATH = Path(__file__).parent.parent.parent.parent.parent / "public.pem"


# Function to load public key from file
def load_public_key():
    with open(PUBLIC_KEY_PATH, "r") as f:
        return f.read()


def verify_jwt_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        # Load the public key
        public_key = load_public_key()

        # Decode the JWT using the public key
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload  # return decoded claims
    except ExpiredSignatureError as e:
        raise HttpUnauthorizationResponse(
            path=str(request.url), message="Token expired"
        )
    except JWTError as e:
        raise HttpUnauthorizationResponse(
            path=str(request.url), message="Invalid token"
        )
