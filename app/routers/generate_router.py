import json
from typing import List, Literal
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.dto.response.error.http_error_response import (
    HttpBadRequestResponse,
    HttpInternalServerError,
    HttpNotFoundResponse,
)
from app.models.user_monthly_subscription import UserMonthlySubscription
from app.services.boto3_client import (
    AmazonPollyTTSRequest,
    AmazonPollyVoice,
    getAmazonPollyVoice,
    querySpeechFromAmazonPolly,
)
from pydantic import BaseModel
from app.middleware.authentication.user.JWT_middleware import verify_jwt_token
from app.middleware.authentication.system.api_key_middleware import api_key_validator


router = APIRouter(
    prefix="/generate",
    tags=["generate"],
    dependencies=[Depends(verify_jwt_token), Depends(api_key_validator)],
    responses={404: {"description": "Not found"}},
)


class AudioRequest(BaseModel):
    text: str
    voice: str = "af_heart"
    lang_code: Literal["a", "j", "z", "f"] = "a"


@router.post("/audio")
async def generate_audio(request: AudioRequest):
    """Generate audio from text and return it as a binary WAV file."""
    return "cat"
    # try:
    #     audio_buffer = text_to_speech(request.text, request.voice, request.lang_code)
    #     return StreamingResponse(audio_buffer, media_type="audio/wav")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


@router.post("/audio/v2")
async def generate_audio_v2(
    request: AmazonPollyTTSRequest,
    payload: dict = Depends(verify_jwt_token),
) -> StreamingResponse:
    try:
        user_raw = payload.get("user", {})
        user = json.loads(user_raw) if isinstance(user_raw, str) else user_raw
        user_uuid = user.get("user_uuid")

        user_subscription = await UserMonthlySubscription.get_user_current_subscription(
            user_uuid
        )

        # * check for user characters use
        if user_subscription == None:
            raise HttpNotFoundResponse(
                message="It seen like you have not subscribe yet"
            )

        if (
            user_subscription.subscription_detail.spent_character
            >= user_subscription.subscription_detail.total_character
        ):
            raise HttpBadRequestResponse(
                message="Look like you touch the limit of the your plan"
            )

        # * check use's plan voice
        polly_voice = await AmazonPollyVoice.find_one({"Id": request.voice_id})

        if polly_voice == None:
            raise HttpNotFoundResponse(message="This voice is not exist")

        character_quantity = len(request.text)

        user_subscription.subscription_detail.spent_character += character_quantity

        await user_subscription.save()

        return StreamingResponse(
            querySpeechFromAmazonPolly(request=request), media_type="audio/mp3"
        )

    except Exception as e:
        raise HttpInternalServerError()


@router.get("/audio/v2/get-voices")
async def getVoice() -> list[AmazonPollyVoice]:
    return await AmazonPollyVoice.find_all().to_list()
