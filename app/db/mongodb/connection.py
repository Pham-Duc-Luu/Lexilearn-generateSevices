from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from typing import List
import os
from beanie import Document, Indexed, init_beanie

from app.models.amazon_polly_voice import AmazonPollyVoice
from app.models.user_monthly_subscription import UserMonthlySubscription


# db = client["text_to_speech__subscription_db"]
# user_monthly_subscriptions_collection = db["user_monthly_subscriptions"]


# tts_voice_collection = db["voices"]


async def initMongoConnection():
    MONGO_URI = os.getenv("MONGO_URI", os.getenv("MONGO_URI"))
    client = AsyncIOMotorClient(MONGO_URI)
    client.get_database
    # Init beanie with the Product document class
    await init_beanie(
        database=client["subscription"],
        document_models=[UserMonthlySubscription, AmazonPollyVoice],
    )
