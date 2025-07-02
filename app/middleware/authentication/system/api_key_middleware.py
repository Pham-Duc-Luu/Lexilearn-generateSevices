from fastapi import HTTPException, Request
import os
from app.dto.response.error.http_error_response import HttpUnauthorizationResponse
from fastapi.responses import JSONResponse

API_KEY = os.getenv("SERVICE_API_KEY")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")


async def api_key_validator(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise HttpUnauthorizationResponse(message="Missing api key")


async def api_subscription_key_validator(request: Request):
    api_key = request.headers.get("x-subscription-key")
    if api_key != SUBSCRIPTION_KEY or api_key == None:
        raise HttpUnauthorizationResponse(
            message="You are not allow to access this api"
        )
