# src/utils/exception_handler.py
# This module handles exceptions for the FastAPI application.

from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import APIException
from .logger import get_logger

log = get_logger(__name__)

async def api_exception_handler(request: Request, exc: APIException):
    """
    Handles custom APIExceptions and returns a standardized JSON response.
    """
    log.error(
        f"API Error: {exc.detail} (Status Code: {exc.status_code})", 
        exc_info=exc
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
# handle any unexpected exceptions
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any unexpected exceptions.
    """
    log.error(f"An unexpected error occurred: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )