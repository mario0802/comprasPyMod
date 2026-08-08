from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.shared.domain.base_entity import BaseEntity

class EstadoSolicitud:
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    ANULADA = "ANULADA"

    VALIDOS = {PENDIENTE, APROBADA, ANULADA}

@dataclass(kw_only=True)
class SolicitudCompraEntity(BaseEntity):
    id: Optional[int] = None
    solicitante_id: int
    fecha_solicitud: datetime = field(default_factory=datetime.utcnow)
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    estado: str = EstadoSolicitud.PENDIENTE
    aprobado_por: Optional[int] = None
    fecha_aprobacion: Optional[datetime] = None
    def __post_init__(self):
        if not self.solicitante_id:
            raise ValueError("El solicitante_id es obligatorio")
        if not self.estado:
            raise ValueError("El estado es obligatorio")
        if self.estado not in EstadoSolicitud.VALIDOS:
            raise ValueError(
                f"Estado inválido: {self.estado}. "
                f"Debe ser uno de {EstadoSolicitud.VALIDOS}"
            )
        if self.monto is not None and self.monto < 0:
            raise ValueError("El monto no puede ser negativo")
        
        if self.estado in (EstadoSolicitud.APROBADA, EstadoSolicitud.ANULADA):
            if not self.aprobado_por:
                raise ValueError(
                    "aprobado_por es obligatorio cuando el estado es "
                    "APROBADA o RECHAZADA"
                )

    def aprobar(self, aprobado_por: int) -> None:
        """Marca la solicitud como aprobada."""
        if self.estado != EstadoSolicitud.PENDIENTE:
            raise ValueError("Solo se puede aprobar una solicitud PENDIENTE")
        self.estado = EstadoSolicitud.APROBADA
        self.aprobado_por = aprobado_por
        self.fecha_aprobacion = datetime.utcnow()

    def rechazar(self, aprobado_por: int) -> None:
        """Marca la solicitud como rechazada."""
        if self.estado != EstadoSolicitud.PENDIENTE:
            raise ValueError("Solo se puede rechazar una solicitud PENDIENTE")
        self.estado = EstadoSolicitud.ANULADA
        self.aprobado_por = aprobado_por
        self.fecha_aprobacion = datetime.utcnow()

    def cancelar(self) -> None:
        """Cancela la solicitud si aún está pendiente."""
        if self.estado != EstadoSolicitud.PENDIENTE:
            raise ValueError("Solo se puede cancelar una solicitud PENDIENTE")
        self.estado = EstadoSolicitud.ANULADA