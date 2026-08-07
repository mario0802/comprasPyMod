import time
import uuid

from flask import Flask, g, request
import structlog

from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


def register_request_logger(app: Flask) -> None:
    @app.before_request
    def _start_request_log():
        # Reusa el request_id entrante (si viene de un gateway/proxy) o genera uno nuevo
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.request_id = request_id
        g.start_time = time.perf_counter()

        # Limpia contexto previo y liga request_id/método/path a TODOS los logs
        # que se emitan durante esta request, sin tener que pasarlos manualmente.
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.path,
        )

        logger.info(
            "request.started",
            remote_addr=request.remote_addr,
            query_params=dict(request.args),
        )

    @app.after_request
    def _end_request_log(response):
        duration_ms = round((time.perf_counter() - g.get("start_time", time.perf_counter())) * 1000, 2)

        logger.info(
            "request.finished",
            status_code=response.status_code,
            duration_ms=duration_ms,
        )
        # Devuelve el request_id al cliente, útil para soporte/debug
        response.headers["X-Request-ID"] = g.get("request_id", "")
        return response

    @app.teardown_request
    def _log_unhandled_exception(exc):
        if exc is not None:
            logger.error("request.unhandled_exception", error=str(exc), exc_info=exc)