from datetime import datetime
from urllib.parse import urlparse

from fastapi import HTTPException
from fastapi.responses import JSONResponse


def safe_decode(obj):
    return obj.decode() if isinstance(obj, bytes) else obj


class HttpExceptionResponse(HTTPException):
    def __init__(self, status: int, error: str, message: str, path: str):
        path = parsed_path = urlparse(path).path  # --> "/some/path"  # <-- Only the path, no host/port/query
        self.JSONResponse = JSONResponse(
            status_code=status,
            content={
                "timestamp": datetime.now().isoformat(),
                "status": safe_decode(status),
                "error": safe_decode(error),
                "message": safe_decode(message),
                "path": safe_decode(path),
            },
        )
        super().__init__(status_code=status, detail=str(message))

    def __str__(self):
        return f"HttpExceptionResponse"


class HttpUnauthorizationResponse(HttpExceptionResponse):

    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 401,
            error: str = "Unauthorization",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization


class HttpBadRequestResponse(HttpExceptionResponse):
    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 400,
            error: str = "Bad request",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization


class HttpForbiddenResponse(HttpExceptionResponse):

    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 403,
            error: str = "Forbidden",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization


class HttpPaymentRequiredResponse(HttpExceptionResponse):

    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 402,
            error: str = "Payment required",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization


class HttpInternalServerError(HttpExceptionResponse):

    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 500,
            error: str = "Internal server error",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization


class HttpNotFoundResponse(HttpExceptionResponse):

    def __init__(
            self,
            message: str = None,
            path: str = None,
            authorization_info: str = None,
            status: int = 404,
            error: str = "Not found",
    ):
        super().__init__(status, error, message, path)
        self.authorization_info = authorization_info  # Optional field to provide additional info about authorization
