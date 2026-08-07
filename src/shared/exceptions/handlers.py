
from __future__ import annotations

from http import HTTPStatus

from flask import Flask
from marshmallow import ValidationError as MarshmallowValidationError
from werkzeug.exceptions import HTTPException

from src.shared.exceptions.base import AppException, InfrastructureException
from src.shared.logging.logger import get_logger
from src.shared.utils.response import error_response

logger = get_logger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Registra todos los error handlers en la instancia de Flask."""

    @app.errorhandler(AppException)
    def handle_app_exception(exc: AppException):
        _log_app_exception(exc)
        return error_response(
            message=exc.message,
            error_code=exc.error_code,
            status_code=exc.status_code,
            details=exc.details,
        )

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation(exc: MarshmallowValidationError):
        # Normaliza errores de Marshmallow al mismo formato que
        # ValidationException, para que el cliente no tenga que
        # distinguir el origen del error.
        logger.warning("validation.error", field_errors=exc.messages)
        return error_response(
            message="Los datos enviados no son válidos.",
            error_code="VALIDATION_ERROR",
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            details={"field_errors": exc.messages},
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        # Errores nativos de Flask/Werkzeug (404 de ruta no encontrada,
        # 405 método no permitido, etc). Se homogeneiza el formato.
        error_code = (exc.name or "HTTP_ERROR").upper().replace(" ", "_")
        logger.info(
            "http.exception",
            error_code=error_code,
            status_code=exc.code,
        )
        return error_response(
            message=exc.description or exc.name,
            error_code=error_code,
            status_code=exc.code or HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_exception(exc: Exception):
        # Última red de seguridad: cualquier excepción no controlada.
        # Nunca se expone el detalle interno/stacktrace al cliente.
        logger.exception("unhandled.exception")
        fallback = InfrastructureException()
        return error_response(
            message=fallback.message,
            error_code=fallback.error_code,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def _log_app_exception(exc: AppException) -> None:
    event = f"app_exception.{exc.error_code.lower()}"
    log_kwargs = dict(
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details,
    )
    if exc.status_code >= 500:
        logger.error(event, exc_info=True, **log_kwargs)
    elif exc.status_code >= 400:
        logger.warning(event, **log_kwargs)
    else:
        logger.info(event, **log_kwargs)