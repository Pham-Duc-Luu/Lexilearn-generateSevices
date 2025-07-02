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

class BasicSubscription(SubscriptionDetail):
    total_character: int = Field(10_000, ge=0)
    spent_character: int = Field(0, ge=0)
    supported_engine: List[Literal["neural", "standard"]] = ["standard"]

class StartSubscription(SubscriptionDetail):
    total_character: int = Field(20_000, ge=0)
    spent_character: int = Field(0, ge=0)
    supported_engine: List[Literal["neural", "standard"]] = ["standard"]

class ProSubscription(SubscriptionDetail):
    total_character: int = Field(50_000, ge=0)
    spent_character: int = Field(0, ge=0)
    supported_engine: List[Literal["neural", "standard"]] = ["standard", "neural"]    

class BussinessSubscription(SubscriptionDetail):
    total_character: int = Field(100_000, ge=0)
    spent_character: int = Field(0, ge=0)
    supported_engine: List[Literal["neural", "standard"]] = ["standard", "neural"]    


class UserMonthlySubscription(Document):

    _id: Optional[Union[str, ObjectId]] = None
    start_date: datetime = None
    end_date: datetime = None
    user_uuid: str
    user_email: EmailStr = None
    subscription_plan: Literal["basic", "start", "pro", "business"] = "basic"
    subscription_detail: SubscriptionDetail = BasicSubscription()

    class Settings:
        name = "user_subscription"

    @classmethod
    async def get_user_current_subscription(
        cls, userUUID: str
    ) -> Optional["UserMonthlySubscription"]:
        now = datetime.now(timezone.utc)
        return await cls.find_one(
            cls.user_uuid == userUUID,
            cls.end_date > now
        )
    



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
        userMonthlySubscription.subscription_detail = BasicSubscription()


    elif subscription_plan == "start":
        userMonthlySubscription.subscription_plan = "start"
        userMonthlySubscription.subscription_detail = StartSubscription()
    elif subscription_plan == "pro":
        userMonthlySubscription.subscription_plan = "pro"
        userMonthlySubscription.subscription_detail = ProSubscription()

    elif subscription_plan == "business":
        userMonthlySubscription.subscription_plan = "business"
        userMonthlySubscription.subscription_detail = BussinessSubscription()
    else:
        raise HttpBadRequestResponse(message="Un-support subscription type")

    return userMonthlySubscription
