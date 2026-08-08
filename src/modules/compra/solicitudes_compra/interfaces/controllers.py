from flask import request, g

from src.modules.compra.solicitudes_compra.application.use_cases.create_solicitud_compra import (
    CreateSolicitudCompraUseCase,
)
from src.modules.compra.solicitudes_compra.application.use_cases.update_solicitud_compra import (
    UpdateSolicitudCompraUseCase,
)
from src.modules.compra.solicitudes_compra.application.use_cases.getById_solicitud_compra import (
    GetSolicitudCompraByIdUseCase,
)
from src.modules.compra.solicitudes_compra.application.use_cases.get_solicitud_compra import (
    ListSolicitudesCompraUseCase
)
from src.modules.compra.solicitudes_compra.application.dto import (
    CrearSolicitudCompraDTO,
    ActualizarSolicitudCompraDTO,
    ListarSolicitudesCompraDTO,
)
from src.modules.compra.solicitudes_compra.interfaces.schemas import (
    CrearSolicitudCompraSchema,
    ActualizarSolicitudCompraSchema,
    ListarSolicitudesCompraSchema,
    SolicitudCompraResponseSchema,
)
from src.shared.utils.response import success_response


class SolicitudCompraController:
    def __init__(
        self,
        create_solicitud_use_case: CreateSolicitudCompraUseCase,
        update_solicitud_use_case: UpdateSolicitudCompraUseCase,
        get_solicitud_by_id_use_case: GetSolicitudCompraByIdUseCase,
        list_solicitudes_use_case: ListSolicitudesCompraUseCase,
    ):
        self.create_solicitud_use_case = create_solicitud_use_case
        self.update_solicitud_use_case = update_solicitud_use_case
        self.get_solicitud_by_id_use_case = get_solicitud_by_id_use_case
        self.list_solicitudes_use_case = list_solicitudes_use_case

    def create(self):
        data = CrearSolicitudCompraSchema().load(request.get_json())

        # TODO: reemplazar por el id del usuario autenticado (g.current_user.id)
        id_usuario_creador = g.current_user_id

        dto = CrearSolicitudCompraDTO(**data, id_usuario_creador=id_usuario_creador)
        result = self.create_solicitud_use_case.execute(dto)

        return success_response(
            data=SolicitudCompraResponseSchema().dump(result),
            status_code=201,
        )

    def update(self, solicitud_id: int):
        data = ActualizarSolicitudCompraSchema().load(request.get_json())

        # TODO: reemplazar por el id del usuario autenticado (g.current_user.id)
        id_usuario_modificador = g.current_user_id

        dto = ActualizarSolicitudCompraDTO(**data, id_usuario_modificador=id_usuario_modificador)
        result = self.update_solicitud_use_case.execute(solicitud_id, dto)

        return success_response(
            data=SolicitudCompraResponseSchema().dump(result),
            status_code=200,
        )

    def get(self, solicitud_id: int):
        result = self.get_solicitud_by_id_use_case.execute(solicitud_id)

        return success_response(
            data=SolicitudCompraResponseSchema().dump(result),
            status_code=200,
        )

    def list(self):
        data = ListarSolicitudesCompraSchema().load(request.args)

        dto = ListarSolicitudesCompraDTO(**data)
        result = self.list_solicitudes_use_case.execute(dto)

        return success_response(
            data=SolicitudCompraResponseSchema(many=True).dump(result),
            status_code=200,
        )