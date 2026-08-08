from src.modules.compra.solicitudes_compra.domain.repositories import SolicitudCompraRepository
from src.modules.compra.solicitudes_compra.domain.exceptions import (
    SolicitudCompraNotFoundException,
    SolicitudCompraInvalidStateException,
)
from src.modules.compra.solicitudes_compra.domain.entities import EstadoSolicitud
from src.modules.compra.solicitudes_compra.application.dto import (
    ActualizarSolicitudCompraDTO,
    SolicitudCompraResponseDTO,
)

class ActualizarSolicitudCompraUseCase:
    def __init__(self, solicitud_repository: SolicitudCompraRepository, session):
        self.solicitud_repository = solicitud_repository
        self.session = session

    def execute(self, solicitud_id: int, dto: ActualizarSolicitudCompraDTO) -> SolicitudCompraResponseDTO:
        solicitud = self.solicitud_repository.get_by_id(solicitud_id)
        if solicitud is None:
            raise SolicitudCompraNotFoundException(solicitud_id)

        # 1. Cambio de estado (si viene en el DTO)
        if dto.estado is not None:
            solicitud = self._procesar_cambio_estado(solicitud, dto)

        # 2. Actualización de datos editables (solo si sigue PENDIENTE)
        if dto.descripcion is not None or dto.monto is not None:
            if solicitud.estado != EstadoSolicitud.PENDIENTE:
                raise SolicitudCompraInvalidStateException(solicitud.estado, "actualizar datos")

            if dto.descripcion is not None:
                solicitud.descripcion = dto.descripcion

            if dto.monto is not None:
                if dto.monto < 0:
                    raise ValueError("El monto no puede ser negativo")
                solicitud.monto = dto.monto

        solicitud.id_usuario_modificador = dto.id_usuario_modificador

        try:
            updated_solicitud = self.solicitud_repository.update(solicitud)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return SolicitudCompraResponseDTO.from_entity(updated_solicitud)

    def _procesar_cambio_estado(self, solicitud, dto: ActualizarSolicitudCompraDTO):
        """Dispatch al método correspondiente de la entidad según el estado destino."""
        try:
            if dto.estado == EstadoSolicitud.APROBADA:
                if not dto.aprobado_por:
                    raise ValueError("aprobado_por es obligatorio para aprobar")
                solicitud.aprobar(aprobado_por=dto.aprobado_por)

            elif dto.estado == EstadoSolicitud.RECHAZADA:
                if not dto.aprobado_por:
                    raise ValueError("aprobado_por es obligatorio para rechazar")
                solicitud.rechazar(aprobado_por=dto.aprobado_por)

            elif dto.estado == EstadoSolicitud.CANCELADA:
                solicitud.cancelar()

            elif dto.estado == EstadoSolicitud.PENDIENTE:
                # No hay transición "volver a pendiente" en la entidad
                raise ValueError("No se puede transicionar manualmente a PENDIENTE")

            else:
                raise ValueError(f"Estado destino inválido: {dto.estado}")

        except ValueError as ex:
            raise SolicitudCompraInvalidStateException(solicitud.estado, f"cambiar a {dto.estado}") from ex
        return solicitud