import logging
import uuid

from fastapi import Request

from app.core.request_context import request_id_context

logger = logging.getLogger(__name__)


async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())

    request.state.request_id = request_id
    token = request_id_context.set(request_id)

    try:
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
            },
        )

        response = await call_next(request)

        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
            },
        )

        response.headers["X-Request-ID"] = request_id

        return response
    finally:
        request_id_context.reset(token)
