from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
from app.dto.response.error.http_error_response import (
    HttpInternalServerError,
    HttpBadRequestResponse,
    HttpNotFoundResponse,
)

from app.middleware.authentication.system.api_key_middleware import (
    api_key_validator,
    api_subscription_key_validator,
)
from app.middleware.authentication.user.JWT_middleware import verify_jwt_token
from app.models.user_monthly_subscription import (
    UserMonthlySubscription,
    createUserMonthlySubscription,
)
from app.utils.convert import convert_mongo_obj

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    dependencies=[
        Depends(verify_jwt_token),
        Depends(api_key_validator),
        Depends(api_subscription_key_validator),
    ],
    responses={404: {"description": "Not found"}},
)


class SubscriptionRequest(BaseModel):
    subscription_plan: Literal["basic", "start", "pro", "business"]


@router.post("")
async def subscription_for_user(
    request: SubscriptionRequest,
    payload: dict = Depends(verify_jwt_token),
):
    try:
        user_raw = payload.get("user", {})
        user = json.loads(user_raw) if isinstance(user_raw, str) else user_raw
        user_uuid = user.get("user_uuid")

        if user_uuid == None:
            raise HttpBadRequestResponse

        now = datetime.now(timezone.utc)

        ## * find any un-expired subscription : end-date > now
        un_expired_subscription = await UserMonthlySubscription.find_one(
            {"user_uuid": user_uuid, "end_date": {"$gt": now}}
        )

        if un_expired_subscription != None:

            return HttpBadRequestResponse(
                message="Subscription have not expired yet!"
            ).JSONResponse

        ## * if all of subscription expired, then allow to subscript

        newSubscription = createUserMonthlySubscription(
            userUUID=user_uuid,
            userEmail=user.get("user_email"),
            subscription_plan=request.subscription_plan,
        )

        result = await newSubscription.insert()

    except Exception as e:
        print(e)
        raise HttpInternalServerError()

    return newSubscription


@router.get("")
async def get_current_subscription(
    payload: dict = Depends(verify_jwt_token),
) -> UserMonthlySubscription:
    user_raw = payload.get("user", {})
    user = json.loads(user_raw) if isinstance(user_raw, str) else user_raw
    # * get user uuid for authentication token
    user_uuid = user.get("user_uuid")
    now = datetime.now(timezone.utc)

    ## * find any un-expired subscription : end-date > now
    un_expired_subscription = (
        await UserMonthlySubscription.get_user_current_subscription(user_uuid)
    )

    if un_expired_subscription == None:
        return HttpNotFoundResponse(message="Your have not subscribe").JSONResponse

    return un_expired_subscription


# @router.get("")
# async def upgrade_user_subscription(
#     request: SubscriptionRequest,
#     payload: dict = Depends(verify_jwt_token),
# ) -> UserMonthlySubscription:
#     user_raw = payload.get("user", {})
#     user = json.loads(user_raw) if isinstance(user_raw, str) else user_raw
#     # * get user uuid for authentication token
#     user_uuid = user.get("user_uuid")
#     now = datetime.now(timezone.utc)

#     ## * find any un-expired subscription : end-date > now
#     un_expired_subscription = await UserMonthlySubscription.find_one(
#         {"user_uuid": user_uuid, "end_date": {"$gt": now}}
#     )

#     return un_expired_subscription
