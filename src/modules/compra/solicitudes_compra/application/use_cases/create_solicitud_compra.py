from src.modules.compra.solicitudes_compra.domain.entities import SolicitudCompraEntity, EstadoSolicitud
from src.modules.compra.solicitudes_compra.domain.repositories import SolicitudCompraRepository
from src.modules.compra.solicitudes_compra.application.dto import (
    CrearSolicitudCompraDTO,
    SolicitudCompraResponseDTO,
)

class CreateSolicitudCompraUseCase:
    def __init__(self, solicitud_repository: SolicitudCompraRepository, session):
        self.solicitud_repository = solicitud_repository
        self.session = session

    def execute(self, dto: CrearSolicitudCompraDTO) -> SolicitudCompraResponseDTO:
        solicitud = SolicitudCompraEntity(
            solicitante_id=dto.solicitante_id,
            descripcion=dto.descripcion,
            monto=dto.monto,
            estado=EstadoSolicitud.PENDIENTE,
            id_usuario_creador=dto.id_usuario_creador,
        )
        try:
            created_solicitud = self.solicitud_repository.create(solicitud)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return SolicitudCompraResponseDTO.from_entity(created_solicitud)