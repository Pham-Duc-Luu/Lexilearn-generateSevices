import io
import os
from typing import List
from dotenv import load_dotenv
import boto3
from pydantic import BaseModel

from app.models.amazon_polly_voice import AmazonPollyVoice

# Load environment variables from .env file
load_dotenv()

# Now use them
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION")

# Create a Polly client
polly = boto3.client(
    "polly",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region,
)

# response = polly.describe_voices()
# for voice in response["Voices"]:
#     print(voice)


class AmazonPollyTTSRequest(BaseModel):
    voice_id: str  # For example, VoiceId like "Joanna"
    text: str  # Text you want to convert to speech
    output_format: str = "mp3"  # Default output format


def querySpeechFromAmazonPolly(request: AmazonPollyTTSRequest) -> io.BytesIO:
    # Call Polly to synthesize speech
    response = polly.synthesize_speech(
        Text=request.text, OutputFormat=request.output_format, VoiceId=request.voice_id
    )

    # Create a BytesIO object to store the audio stream
    audio_stream = io.BytesIO(response["AudioStream"].read())

    # Return the audio as a BytesIO object
    return audio_stream


def getAmazonPollyVoice() -> List[AmazonPollyVoice]:
    voices_raw = polly.describe_voices()["Voices"]
    return [AmazonPollyVoice(**voice) for voice in voices_raw]


async def is_user_allow_to_access_voice(userUUID: str, voiceId: str) -> bool:

    return True
