from typing import Set
from app.models.amazon_polly_voice import AmazonPollyVoice
from app.services.boto3_client import getAmazonPollyVoice
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio


async def update_available_voices_to_mongo():
    # * get all amazon polly voices available
    voices = getAmazonPollyVoice()
    await AmazonPollyVoice.delete_all()
    for voice in voices:
        await voice.insert()


async def repeating_job():
    while True:
        await update_available_voices_to_mongo()
        await asyncio.sleep(2 * 60 * 60)  # 2 hours


# Setup the scheduler
def start_scheduler():
    # * add the repeating job into queue so that it can be repeat
    asyncio.create_task(repeating_job())
