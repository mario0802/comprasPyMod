from src.modules.compra.solicitudes_compra.domain.repositories import SolicitudCompraRepository
from src.modules.compra.solicitudes_compra.domain.exceptions import SolicitudCompraNotFoundException
from src.modules.compra.solicitudes_compra.application.dto import SolicitudCompraResponseDTO


class GetSolicitudCompraByIdUseCase:
    def __init__(self, solicitud_repository: SolicitudCompraRepository):
        self.solicitud_repository = solicitud_repository

    def execute(self, solicitud_id: int) -> SolicitudCompraResponseDTO:
        solicitud = self.solicitud_repository.get_by_id(solicitud_id)
        if solicitud is None:
            raise SolicitudCompraNotFoundException(solicitud_id)

        return SolicitudCompraResponseDTO.from_entity(solicitud)