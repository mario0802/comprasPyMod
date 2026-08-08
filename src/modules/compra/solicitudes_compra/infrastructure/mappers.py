from src.modules.compra.solicitudes_compra.domain.entities import SolicitudCompraEntity
from src.modules.compra.solicitudes_compra.infrastructure.models import SolicitudCompraModel


class SolicitudCompraMapper:
    """Traduce entre SolicitudCompraModel (infraestructura/Postgres) y SolicitudCompraEntity (dominio)."""

    @staticmethod
    def to_entity(model: SolicitudCompraModel) -> SolicitudCompraEntity:
        return SolicitudCompraEntity(
            id=model.id,
            solicitante_id=model.solicitante_id,
            fecha_solicitud=model.fecha_solicitud,
            descripcion=model.descripcion,
            monto=model.monto,
            estado=model.estado,
            aprobado_por=model.aprobado_por,
            fecha_aprobacion=model.fecha_aprobacion,
            id_usuario_creador=model.id_usuario_creador,
            fecha_creacion=model.fecha_creacion,
            id_usuario_modificador=model.id_usuario_modificador,
            fecha_modificacion=model.fecha_modificacion,
        )

    @staticmethod
    def to_model(entity: SolicitudCompraEntity) -> SolicitudCompraModel:
        return SolicitudCompraModel(
            id=entity.id,
            solicitante_id=entity.solicitante_id,
            fecha_solicitud=entity.fecha_solicitud,
            descripcion=entity.descripcion,
            monto=entity.monto,
            estado=entity.estado,
            aprobado_por=entity.aprobado_por,
            fecha_aprobacion=entity.fecha_aprobacion,
            id_usuario_creador=entity.id_usuario_creador,
            fecha_creacion=entity.fecha_creacion,
            id_usuario_modificador=entity.id_usuario_modificador,
            fecha_modificacion=entity.fecha_modificacion,
        )