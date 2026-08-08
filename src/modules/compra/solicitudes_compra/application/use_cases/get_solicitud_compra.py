from src.modules.compra.solicitudes_compra.domain.repositories import SolicitudCompraRepository
from src.modules.compra.solicitudes_compra.application.dto import (
    ListarSolicitudesCompraDTO,
    SolicitudCompraResponseDTO,
)


class ListSolicitudesCompraUseCase:
    def __init__(self, solicitud_repository: SolicitudCompraRepository):
        self.solicitud_repository = solicitud_repository

    def execute(self, dto: ListarSolicitudesCompraDTO) -> list[SolicitudCompraResponseDTO]:
        if dto.solicitante_id is not None:
            solicitudes = self.solicitud_repository.list_by_solicitante(
                solicitante_id=dto.solicitante_id,
                limit=dto.limit,
                offset=dto.offset,
            )
        elif dto.estado is not None:
            solicitudes = self.solicitud_repository.list_by_estado(
                estado=dto.estado,
                limit=dto.limit,
                offset=dto.offset,
            )
        else:
            solicitudes = self.solicitud_repository.list_all(
                limit=dto.limit,
                offset=dto.offset,
            )

        return [SolicitudCompraResponseDTO.from_entity(s) for s in solicitudes]