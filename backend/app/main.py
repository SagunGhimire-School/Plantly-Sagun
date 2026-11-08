import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from app.ai import GeminiAdapter
from app.auth import router as auth_router
from app.db import engine
from app.growing import router as growing_router

app = FastAPI(title="Plantly API", version="0.1.0")
app.include_router(auth_router)
app.include_router(growing_router)


def error_response(code, message, status, fields=None):
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": code,
                "message": message,
                "fields": fields or {},
                "request_id": str(uuid.uuid4()),
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_error(request: Request, error: HTTPException):
    return error_response(
        str(error.detail), str(error.detail).replace("_", " ").capitalize(), error.status_code
    )


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, error: RequestValidationError):
    fields = {".".join(map(str, item["loc"][1:])): item["msg"] for item in error.errors()}
    return error_response("INVALID_INPUT", "Check the highlighted information.", 422, fields)


@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, error: SQLAlchemyError):
    return error_response(
        "DATABASE_UNAVAILABLE", "The database is unavailable. Please try again.", 503
    )


@app.middleware("http")
async def request_limits(request: Request, call_next):
    # Bound both fixed-length and chunked input before parsing passwords or JSON.
    size = 0
    chunks = []
    async for chunk in request.stream():
        size += len(chunk)
        if size > 65536:
            return error_response("BODY_TOO_LARGE", "Request exceeds 64 KiB.", 413)
        chunks.append(chunk)
    request._body = b"".join(chunks)
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/health")
def liveness():
    return {"status": "ok"}


@app.get("/api/v1/health")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503, content={"status": "unavailable", "database": "unavailable"}
        )
    return {"status": "ok", "database": "connected"}


@app.get("/api/v1/capabilities")
def capabilities():
    return {
        "planning": GeminiAdapter().status(),
        "weather": "unavailable",
        "prices": "unavailable",
        "scientific_rules": "not_reviewed",
    }
