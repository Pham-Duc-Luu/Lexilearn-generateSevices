from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, List, Literal
from datetime import datetime, timezone
from typing import Optional, Union
from dateutil.relativedelta import relativedelta
from typing import Optional  # optional for clarity (Python < 3.10)
from app.dto.response.error.http_error_response import HttpBadRequestResponse
from beanie import Document, Indexed, init_beanie


class SubscriptionDetail(BaseModel):
    total_character: int = Field(..., ge=0)
    spent_character: int = Field(..., ge=0)
    supported_engine: List[Literal["neural", "standard"]]


class UserMonthlySubscription(Document):
    _id: Optional[Union[str, ObjectId]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_uuid: Annotated[str, Indexed(unique=True)]
    user_email: Optional[EmailStr] = None
    subscription_plan: Optional[Literal["basic", "start", "pro", "business"]] = None
    subscription_detail: Optional[SubscriptionDetail] = None

    class Settings:
        name = "user_subscription"

    @classmethod
    async def get_user_current_subscription(
        cls, userUUID: str
    ) -> Optional["UserMonthlySubscription"]:
        now = datetime.now(timezone.utc)
        return await cls.find_one({"user_uuid": userUUID, "end_date": {"$gt": now}})


def createUserMonthlySubscription(
    userUUID: str,
    userEmail: str,
    subscription_plan: Literal["basic", "start", "pro", "business"],
) -> UserMonthlySubscription:
    userMonthlySubscription = UserMonthlySubscription(
        start_date=datetime.now(timezone.utc),
        end_date=(datetime.now(timezone.utc) + relativedelta(months=1)),
        user_uuid=userUUID,
        user_email=userEmail,
    )
    if subscription_plan == "basic":
        userMonthlySubscription.subscription_plan = "basic"
        userMonthlySubscription.subscription_detail = SubscriptionDetail(
            spent_character=0, supported_engine=["standard"], total_character=10_000
        )
    elif subscription_plan == "start":
        userMonthlySubscription.subscription_plan = "start"
        userMonthlySubscription.subscription_detail = SubscriptionDetail(
            spent_character=0, supported_engine=["standard"], total_character=20_000
        )
    elif subscription_plan == "pro":
        userMonthlySubscription.subscription_plan = "pro"
        userMonthlySubscription.subscription_detail = SubscriptionDetail(
            spent_character=0,
            supported_engine=["standard", "neural"],
            total_character=50_000,
        )

    elif subscription_plan == "business":
        userMonthlySubscription.subscription_plan = "business"
        userMonthlySubscription.subscription_detail = SubscriptionDetail(
            spent_character=0,
            supported_engine=["standard", "neural"],
            total_character=100_000,
        )
    else:
        raise HttpBadRequestResponse(message="Un-support subscription type")

    return userMonthlySubscription
