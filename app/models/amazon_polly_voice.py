from typing import Annotated
from beanie import Document, Indexed
import pymongo
from beanie import Document, Indexed


class AmazonPollyVoice(Document):
    Gender: str
    Id: str
    LanguageCode: str
    LanguageName: str
    Name: str
    SupportedEngines: list[str]

    class Settings:
        name = "amazon_polly_voices"
