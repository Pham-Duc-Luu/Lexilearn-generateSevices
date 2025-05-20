import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from app.config.logger import logger
# from app.config.logger import loggerConfigInit
from app.db.mongodb.connection import initMongoConnection
from app.dto.response.error.http_error_response import HttpExceptionResponse
from app.middleware.logginMiddleware import LoggingMiddleware
from app.schedule.update_voice import start_scheduler
from .routers import generate_router, subscription

# Load environment variables from .env file

load_dotenv()
app = FastAPI(title="Text-to-Speech API")


## Custom exception handler
@app.exception_handler(HttpExceptionResponse)
async def global_exception_handler(request: Request, exc: HttpExceptionResponse):
    logger.error(f"HTTP Exception: {exc.JSONResponse.body}")
    return exc.JSONResponse


# init logger service
# ! run init only one
# loggerConfigInit()

# Register API routes
app.include_router(generate_router.router)
app.include_router(subscription.router)

# app middleware
app.add_middleware(LoggingMiddleware)


## start-up services
@app.on_event("startup")
async def startup():
    await initMongoConnection()
    start_scheduler()


@app.get("/")
async def root():
    logger.info("Root access")
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app)
