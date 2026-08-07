
from __future__ import annotations

from http import HTTPStatus
from typing import Any


class AppException(Exception):
    """
    Excepción base de toda la aplicación.

    Attributes:
        message: Mensaje legible para humanos (puede exponerse al cliente).
        status_code: Código HTTP que debe devolver el error_handler.
        error_code: Código corto identificador del error, útil para el
            frontend/cliente API (no cambia entre idiomas).
        details: Información adicional estructurada (ej. errores de
            validación por campo, metadata de contexto, etc).
    """

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str | None = None,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self._default_message()
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.details = details or {}
        super().__init__(self.message)

    def _default_message(self) -> str:
        return "Ocurrió un error inesperado."

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "error_code": self.error_code,
            "message": self.message,
        }
        if self.details:
            payload["details"] = self.details
        return payload

    def __repr__(self) -> str:  # pragma: no cover - solo debug
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, status_code={self.status_code}, "
            f"error_code={self.error_code!r})"
        )


# ---------------------------------------------------------------------------
# Excepciones genéricas de capa (application / domain / infrastructure)
# ---------------------------------------------------------------------------


class DomainException(AppException):
    """
    Error que viola una regla de negocio del dominio.

    Ej: "no se puede cancelar una orden ya entregada".
    Debe lanzarse desde entidades/servicios de dominio, nunca desde la capa
    de infraestructura o interfaces.
    """

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    error_code = "DOMAIN_ERROR"

    def _default_message(self) -> str:
        return "La operación viola una regla de negocio."


class ApplicationException(AppException):
    """
    Error de orquestación en la capa de aplicación (use cases).

    Ej: un use case que coordina dos repositorios y detecta un estado
    inconsistente entre ellos.
    """

    status_code = HTTPStatus.BAD_REQUEST  # 400
    error_code = "APPLICATION_ERROR"

    def _default_message(self) -> str:
        return "No fue posible completar la operación solicitada."


class InfrastructureException(AppException):
    """
    Error técnico en la capa de infraestructura.

    Ej: falla de conexión a base de datos, timeout a un servicio externo,
    error al parsear un archivo, etc. Normalmente NO se expone el detalle
    técnico real al cliente (se loggea internamente).
    """

    status_code = HTTPStatus.SERVICE_UNAVAILABLE  # 503
    error_code = "INFRASTRUCTURE_ERROR"

    def _default_message(self) -> str:
        return "Un servicio interno no está disponible en este momento."


# ---------------------------------------------------------------------------
# Excepciones específicas y reutilizables entre módulos
# ---------------------------------------------------------------------------


class NotFoundException(DomainException):
    """El recurso solicitado no existe."""

    status_code = HTTPStatus.NOT_FOUND  # 404
    error_code = "NOT_FOUND"

    def __init__(
        self,
        message: str | None = None,
        *,
        resource: str | None = None,
        resource_id: Any = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {}) or {}
        if resource:
            details.setdefault("resource", resource)
        if resource_id is not None:
            details.setdefault("resource_id", resource_id)

        if message is None and resource:
            message = f"{resource} no encontrado."
            if resource_id is not None:
                message = f"{resource} con id '{resource_id}' no encontrado."

        super().__init__(message, details=details, **kwargs)

    def _default_message(self) -> str:
        return "Recurso no encontrado."


class AlreadyExistsException(DomainException):
    """El recurso que se intenta crear ya existe (conflicto)."""

    status_code = HTTPStatus.CONFLICT  # 409
    error_code = "ALREADY_EXISTS"

    def _default_message(self) -> str:
        return "El recurso ya existe."


class ValidationException(ApplicationException):
    """
    Error de validación de datos de entrada.

    `details` debería contener el detalle por campo, ej:
        {"field_errors": {"email": ["formato inválido"]}}
    """

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    error_code = "VALIDATION_ERROR"

    def __init__(
        self,
        message: str | None = None,
        *,
        field_errors: dict[str, list[str]] | None = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {}) or {}
        if field_errors:
            details.setdefault("field_errors", field_errors)
        super().__init__(message, details=details, **kwargs)

    def _default_message(self) -> str:
        return "Los datos enviados no son válidos."


class UnauthorizedException(AppException):
    """El usuario no está autenticado o el token es inválido/expiró."""

    status_code = HTTPStatus.UNAUTHORIZED  # 401
    error_code = "UNAUTHORIZED"

    def _default_message(self) -> str:
        return "No autenticado. Se requiere iniciar sesión."


class ForbiddenException(AppException):
    """El usuario está autenticado pero no tiene permisos suficientes."""

    status_code = HTTPStatus.FORBIDDEN  # 403
    error_code = "FORBIDDEN"

    def _default_message(self) -> str:
        return "No tiene permisos para realizar esta acción."


class BusinessRuleException(DomainException):
    """
    Violación explícita de una regla de negocio nombrada.

    Útil cuando quieres dar contexto de *qué* regla se violó, ej:
        raise BusinessRuleException(rule="ORDER_MUST_BE_PAID_BEFORE_SHIP")
    """

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    error_code = "BUSINESS_RULE_VIOLATION"

    def __init__(
        self,
        message: str | None = None,
        *,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {}) or {}
        if rule:
            details.setdefault("rule", rule)
        super().__init__(message, details=details, **kwargs)

    def _default_message(self) -> str:
        return "No se cumple una regla de negocio requerida."


class ExternalServiceException(InfrastructureException):
    """
    Falla al comunicarse con un servicio externo (API de terceros, etc).
    """

    status_code = HTTPStatus.BAD_GATEWAY  # 502
    error_code = "EXTERNAL_SERVICE_ERROR"

    def __init__(
        self,
        message: str | None = None,
        *,
        service_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {}) or {}
        if service_name:
            details.setdefault("service_name", service_name)
        super().__init__(message, details=details, **kwargs)

    def _default_message(self) -> str:
        return "Error al comunicarse con un servicio externo."