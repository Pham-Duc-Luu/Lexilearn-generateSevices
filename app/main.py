from fastapi import FastAPI, Depends, Request
from typing import Union
import uvicorn
from dotenv import load_dotenv
from app.db.mongodb.connection import initMongoConnection
from app.dto.response.error.http_error_response import HttpExceptionResponse
from app.middleware.authentication.system.api_key_middleware import api_key_validator
from app.schedule.update_voice import start_scheduler

from .routers import generate_router, subscription

# Load environment variables from .env file


load_dotenv()
app = FastAPI(title="Text-to-Speech API")


## Custom exception handler
@app.exception_handler(HttpExceptionResponse)
async def global_exception_handler(request: Request, exc: HttpExceptionResponse):
    return exc.JSONResponse


# Register API routes
app.include_router(generate_router.router)
app.include_router(subscription.router)


## start-up services
@app.on_event("startup")
async def startup():
    await initMongoConnection()
    start_scheduler()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
