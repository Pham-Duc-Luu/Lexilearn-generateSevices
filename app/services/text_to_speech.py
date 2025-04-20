import io
import soundfile as sf
from kokoro import KPipeline
from typing import Literal

def text_to_speech(text: str, voice: str = "af_heart", lang_code: Literal['a', 'j', 'z', 'f'] = 'a') -> io.BytesIO:
    print(lang_code)
    # Initialize Kokoro Pipeline
    pipeline = KPipeline(lang_code=lang_code)

    """Generate speech from text and return it as an in-memory WAV file."""
    generator = pipeline(text, voice=voice)
    print(text)
    audio_buffer = io.BytesIO()

    for _, _, audio in generator:
        sf.write(audio_buffer, audio, 24000, format="WAV")

    # Move the buffer pointer to the beginning
    audio_buffer.seek(0)
    return audio_buffer
