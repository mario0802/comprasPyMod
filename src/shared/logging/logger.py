"""
Configuración central de logging para todo el monolito modular.

- Usa `structlog` sobre el `logging` estándar de Python.
- En desarrollo: salida en consola, coloreada y legible (ConsoleRenderer).
- En producción/staging: salida en JSON (fácil de indexar en ELK/Datadog/CloudWatch).
- Cada módulo (users, orders, etc.) obtiene su logger con `get_logger(__name__)`
  y automáticamente queda "atado" (bound) a la request actual gracias al
  middleware de request_logger (request_id, path, method, etc.).
Uso típico dentro de un módulo:
    from src.shared.logging.logger import get_logger
    logger = get_logger(__name__)
    def create_user(...):
        logger.info("user.create.started", email=email)
        ...
        logger.info("user.create.success", user_id=user.id)
"""
from __future__ import annotations
import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor
from src.config.settings import settings

def _drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    """
    Uvicorn/Werkzeug a veces inyectan 'color_message'; lo eliminamos
    para no duplicar el mensaje en la salida estructurada.
    """
    event_dict.pop("color_message", None)
    return event_dict


def _add_app_context(_, __, event_dict: EventDict) -> EventDict:
    """Agrega metadata fija de la aplicación a cada log."""
    event_dict.setdefault("app", settings.APP_NAME)
    event_dict.setdefault("env", settings.ENV)
    return event_dict


def configure_logging() -> None:
    """
    Configura structlog + logging estándar.
    Debe llamarse UNA sola vez, apenas arranca la app (en create_app()).
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # permite bind por request (request_id, etc.)
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _add_app_context,
        _drop_color_message_key,
    ]

    if settings.LOG_JSON:
        # Producción / staging: una línea JSON por log
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        # Desarrollo: legible y coloreado en consola
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Silenciar ruido de librerías de terceros que son muy verbosas
    for noisy_logger in ("werkzeug", "urllib3", "sqlalchemy.engine"):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)


def get_logger(name: str | None = None, **initial_context: Any) -> structlog.stdlib.BoundLogger:
    """
    Factory para obtener un logger estructurado.

    Args:
        name: normalmente __name__ del módulo que lo usa.
        **initial_context: pares clave-valor que quedarán "pegados"
            a todos los logs emitidos por este logger (ej: module="users").

    Returns:
        Un BoundLogger de structlog listo para usar.
    """
    logger = structlog.get_logger(name)
    if initial_context:
        logger = logger.bind(**initial_context)
    return logger