from typing import Optional

from sqlalchemy.orm import Session

from src.modules.compra.solicitudes_compra.domain.entities import SolicitudCompraEntity
from src.modules.compra.solicitudes_compra.domain.repositories import SolicitudCompraRepository
from src.modules.compra.solicitudes_compra.infrastructure.models import SolicitudCompraModel
from src.modules.compra.solicitudes_compra.infrastructure.mappers import SolicitudCompraMapper


class SQLAlchemySolicitudCompraRepository(SolicitudCompraRepository):
    """
    Implementación concreta de SolicitudCompraRepository usando SQLAlchemy + Postgres.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, solicitud_id: int) -> Optional[SolicitudCompraEntity]:
        model = self.session.query(SolicitudCompraModel).filter_by(id=solicitud_id).first()
        return SolicitudCompraMapper.to_entity(model) if model else None

    def create(self, solicitud: SolicitudCompraEntity) -> SolicitudCompraEntity:
        model = SolicitudCompraMapper.to_model(solicitud)
        self.session.add(model)
        self.session.flush()  # para obtener el id generado sin hacer commit todavía
        return SolicitudCompraMapper.to_entity(model)

    def update(self, solicitud: SolicitudCompraEntity) -> SolicitudCompraEntity:
        model = self.session.query(SolicitudCompraModel).filter_by(id=solicitud.id).first()
        if model is None:
            raise ValueError(f"Solicitud de compra con id '{solicitud.id}' no encontrada")

        model.solicitante_id = solicitud.solicitante_id
        model.descripcion = solicitud.descripcion
        model.monto = solicitud.monto
        model.estado = solicitud.estado
        model.aprobado_por = solicitud.aprobado_por
        model.fecha_aprobacion = solicitud.fecha_aprobacion
        model.id_usuario_modificador = solicitud.id_usuario_modificador
        model.fecha_modificacion = solicitud.fecha_modificacion

        self.session.flush()
        return SolicitudCompraMapper.to_entity(model)

    def delete(self, solicitud_id: int) -> None:
        model = self.session.query(SolicitudCompraModel).filter_by(id=solicitud_id).first()
        if model is None:
            raise ValueError(f"Solicitud de compra con id '{solicitud_id}' no encontrada")
        self.session.delete(model)
        self.session.flush()

    def list_all(self, limit: int = 100, offset: int = 0) -> list[SolicitudCompraEntity]:
        models = self.session.query(SolicitudCompraModel).limit(limit).offset(offset).all()
        return [SolicitudCompraMapper.to_entity(m) for m in models]

    def list_by_solicitante(
        self, solicitante_id: int, limit: int = 100, offset: int = 0
    ) -> list[SolicitudCompraEntity]:
        models = (
            self.session.query(SolicitudCompraModel)
            .filter_by(solicitante_id=solicitante_id)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [SolicitudCompraMapper.to_entity(m) for m in models]

    def list_by_estado(
        self, estado: str, limit: int = 100, offset: int = 0
    ) -> list[SolicitudCompraEntity]:
        models = (
            self.session.query(SolicitudCompraModel)
            .filter_by(estado=estado)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [SolicitudCompraMapper.to_entity(m) for m in models]