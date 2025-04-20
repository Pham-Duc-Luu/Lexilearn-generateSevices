from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.text_to_speech import text_to_speech
from pydantic import BaseModel


router = APIRouter(
    prefix="/generate",
    tags=["generate"],
          responses={404: {"description": "Not found"}},
)

class AudioRequest(BaseModel):
    text: str
    voice: str = "af_heart"
    lang_code: Literal['a', 'j', 'z', 'f'] = 'a'


@router.post("/audio")
async def generate_audio(request: AudioRequest):
    """Generate audio from text and return it as a binary WAV file."""
    try:
        audio_buffer = text_to_speech(request.text, request.voice, request.lang_code)
        return StreamingResponse(audio_buffer, media_type="audio/wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
