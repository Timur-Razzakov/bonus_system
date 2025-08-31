from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import ValidationError

from apps.core.config import settings
from apps.core.exceptions.handler import hande_exception
from apps.core.exceptions.message_exception import MessageException


def bootstrap_fastapi(include_router: APIRouter):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        debug=settings.DEBUG_FAST_API,
    )
    app.include_router(include_router)
    register_exception_handlers(app)

    return app


def register_exception_handlers(app):
    app.add_exception_handler(Exception, hande_exception)
    app.add_exception_handler(MessageException, hande_exception)
    app.add_exception_handler(ValidationError, hande_exception)
    app.add_exception_handler(HTTPException, hande_exception)
