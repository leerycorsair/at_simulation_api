import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from at_simulation_api.config.logger import application_logger as logger
from at_simulation_api.core.errors import Error, InternalServerError


def redact_headers(headers: dict) -> dict:
    return {
        key: (value if key.lower() != "authorization" else "")
        for key, value in headers.items()
    }


def log_request(details: dict, level: str = "info"):
    if level == "info":
        logger.info("Request Dump", extra={"details": details})
    elif level == "error":
        logger.error("Request Dump", extra={"details": details})


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        try:
            request_body = await request.json() if await request.body() else "empty"
        except Exception as e:
            request_body = str(e)

        try:
            response = await call_next(request)

            log_request(
                {
                    "status_code": response.status_code,
                    "method": request.method,
                    "url": str(request.url),
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "request_body": request_body,
                },
                level="info",
            )
            return response

        except Error as custom_error:
            log_request(
                {
                    "status_code": custom_error.status_code,
                    "error_message": str(custom_error),
                    "error_details": custom_error.error_details,
                    "method": request.method,
                    "url": str(request.url),
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "headers": redact_headers(request.headers),
                    "request_body": request_body,
                },
                level="error",
            )
            raise custom_error

        except Exception as unexpected_error:
            internal_error = InternalServerError(str(unexpected_error))
            log_request(
                {
                    "status_code": internal_error.status_code,
                    "error_message": str(internal_error),
                    "method": request.method,
                    "url": str(request.url),
                    "client_ip": client_ip,
                    "client_port": client_port,
                    "headers": redact_headers(request.headers),
                    "request_body": request_body,
                    "trace": traceback.format_exc(),
                },
                level="error",
            )
            raise internal_error
