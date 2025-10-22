from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union

class TodoNotFoundException(HTTPException):
    def __init__(self, todo_id: int):
        super().__init__(
            status_code=404,
            detail=f"Todo with id {todo_id} not found"
        )

class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail
        )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "status_code": exc.status_code
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "ValidationError",
                "message": "Validation error",
                "details": exc.errors()
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An internal server error occurred",
                "status_code": 500
            }
        }
    )
