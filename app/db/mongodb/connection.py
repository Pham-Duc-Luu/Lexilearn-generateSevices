from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from typing import List
import os
from beanie import Document, Indexed, init_beanie
from app.config.logger import logger
from app.models.amazon_polly_voice import AmazonPollyVoice
from app.models.user_monthly_subscription import UserMonthlySubscription


async def initMongoConnection():
    try :
       
        MONGO_URI = os.getenv("MONGO_URI", os.getenv("MONGO_URI"))

        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set.")
        
        client = AsyncIOMotorClient(MONGO_URI)
        client.get_database
        # Init beanie with the Product document class
        await init_beanie(
            database=client[ os.getenv("MONGO_DB")],
            document_models=[UserMonthlySubscription, AmazonPollyVoice],
        )
        
        logger.info("✅ Successfully connected to MongoDB and initialized Beanie.")

    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise
