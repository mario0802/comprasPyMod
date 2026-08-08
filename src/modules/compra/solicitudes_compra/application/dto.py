from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(kw_only=True)
class CrearSolicitudCompraDTO:
    """DTO de entrada para crear una nueva solicitud de compra."""
    solicitante_id: int
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    id_usuario_creador:int

@dataclass(kw_only=True)
class ActualizarSolicitudCompraDTO:
    """DTO de entrada para actualizar datos editables de una solicitud (mientras esté PENDIENTE)."""
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    descripcion: Optional[str]
    estado: Optional[str] = None
    aprobado_por: Optional[int]
    id_usuario_modificador:int

@dataclass
class AprobarSolicitudCompraDTO:
    """DTO de entrada para aprobar una solicitud."""
    aprobado_por: int

@dataclass
class RechazarSolicitudCompraDTO:
    """DTO de entrada para rechazar una solicitud."""
    aprobado_por: int

@dataclass
class ListarSolicitudesCompraDTO:
    """DTO de entrada para filtrar/paginar el listado de solicitudes."""
    solicitante_id: Optional[int] = None
    estado: Optional[str] = None
    limit: int = 100
    offset: int = 0

@dataclass
class SolicitudCompraResponseDTO:
    """DTO de salida: representación pública de una solicitud de compra."""
    id: int
    solicitante_id: int
    fecha_solicitud: datetime
    descripcion: Optional[str]
    monto: Optional[Decimal]
    estado: str
    aprobado_por: Optional[int]
    fecha_aprobacion: Optional[datetime]
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    @staticmethod
    def from_entity(entity) -> "SolicitudCompraResponseDTO":
        return SolicitudCompraResponseDTO(
            id=entity.id,
            solicitante_id=entity.solicitante_id,
            fecha_solicitud=entity.fecha_solicitud,
            descripcion=entity.descripcion,
            monto=entity.monto,
            estado=entity.estado,
            aprobado_por=entity.aprobado_por,
            fecha_aprobacion=entity.fecha_aprobacion,
            fecha_creacion=entity.fecha_creacion,
            fecha_modificacion=entity.fecha_modificacion,
        )