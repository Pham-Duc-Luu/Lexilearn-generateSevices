import time
from urllib.request import Request

from starlette.middleware.base import BaseHTTPMiddleware

from app.config.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"in {duration:.3f}s"
        )
        return response
