from fastapi import HTTPException, Request
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse

from apps.core.exceptions.message_exception import MessageException


class ErrorModel(BaseModel):
    message_id: str
    kwargs: dict | None = None


def hande_exception(request: Request, exc: Exception):
    try:
        if isinstance(exc, MessageException):
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorModel(message_id=exc.message_id).model_dump(),
            )
        elif isinstance(exc, ValidationError):
            return JSONResponse(
                status_code=422,
                content=ErrorModel(message_id="VALIDATION_ERROR", kwargs={"error": str(exc)}).model_dump(),
            )
        elif isinstance(exc, HTTPException):
            if exc.status_code == 404:
                return JSONResponse(
                    status_code=404,
                    content=ErrorModel(
                        message_id="NOT_FOUND",
                    ).model_dump(),
                )
            elif exc.status_code == 422:
                return JSONResponse(
                    status_code=422,
                    content=ErrorModel(message_id="VALIDATION_ERROR", kwargs={"error": exc}).model_dump(),
                )
            elif exc.status_code == 401:
                return JSONResponse(
                    status_code=401,
                    content=ErrorModel(
                        message_id="UNAUTHENTICATED",
                    ).model_dump(),
                )
            elif exc.status_code == 403:
                return JSONResponse(
                    status_code=403,
                    content=ErrorModel(
                        message_id="UNAUTHORIZED",
                    ).model_dump(),
                )
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorModel(message_id="INTERNAL_SERVER_ERROR").model_dump(),
            )
        else:
            return JSONResponse(
                status_code=500,
                content=ErrorModel(message_id="INTERNAL_SERVER_ERROR").model_dump(),
            )
    except AttributeError:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorModel(message_id="INTERNAL_SERVER_ERROR").model_dump(),
        )
