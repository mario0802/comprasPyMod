from src.shared.exceptions.base import DomainException, UnauthorizedException, ValidationException

class SolicitudCompraNotFoundException(DomainException):
    def __init__(self, solicitud_id: int):
        super().__init__(f"Solicitud de compra con id '{solicitud_id}' no encontrada")

class SolicitudCompraInvalidStateException(DomainException):
    def __init__(self, estado_actual: str, accion: str):
        super().__init__(
            f"No se puede '{accion}' una solicitud en estado '{estado_actual}'"
        )

class SolicitudCompraAlreadyProcessedException(DomainException):
    def __init__(self, solicitud_id: int, estado_actual: str):
        super().__init__(
            f"La solicitud '{solicitud_id}' ya fue procesada (estado: '{estado_actual}')"
        )

class MontoInvalidoException(ValidationException):
    def __init__(self, monto):
        super().__init__(f"El monto '{monto}' no es válido, debe ser mayor o igual a 0")

class AprobadorNoAutorizadoException(UnauthorizedException):
    def __init__(self):
        super().__init__("El usuario no tiene permisos para aprobar/rechazar solicitudes")

class SolicitanteInvalidoException(DomainException):
    def __init__(self):
        super().__init__("El solicitante_id es obligatorio y debe ser válido")