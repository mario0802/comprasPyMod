from flask_smorest import Blueprint

from src.modules.compra.solicitudes_compra.interfaces.controllers import SolicitudCompraController
from src.modules.compra.solicitudes_compra.interfaces.schemas import (
    CrearSolicitudCompraSchema,
    ActualizarSolicitudCompraSchema,
    ListarSolicitudesCompraSchema,
)
from src.config.container import container
from src.shared.auth.decorators import require_auth

solicitudes_compra_bp = Blueprint(
    "solicitudes_compra", __name__,
    url_prefix="/api/solicitudes-compra",
    description="Gestión de solicitudes de compra"
)


def _controller() -> SolicitudCompraController:
    return container.get_solicitud_compra_controller()


@solicitudes_compra_bp.route("", methods=["POST"])
@solicitudes_compra_bp.arguments(CrearSolicitudCompraSchema)
@solicitudes_compra_bp.doc(responses={201: {"description": "Solicitud creada exitosamente"}})
@require_auth
def create_solicitud(new_data):
    """Crea una nueva solicitud de compra"""
    return _controller().create(new_data)


@solicitudes_compra_bp.route("/<int:solicitud_id>", methods=["PATCH"])
@solicitudes_compra_bp.arguments(ActualizarSolicitudCompraSchema)
@solicitudes_compra_bp.doc(responses={200: {"description": "Solicitud actualizada"}})
@require_auth
def update_solicitud(update_data, solicitud_id: int):
    """Actualiza una solicitud de compra existente"""
    return _controller().update(solicitud_id, update_data)


@solicitudes_compra_bp.route("/<int:solicitud_id>", methods=["GET"])
@solicitudes_compra_bp.doc(responses={200: {"description": "Solicitud encontrada"}})
@require_auth
def get_solicitud(solicitud_id: int):
    """Obtiene una solicitud de compra por id"""
    return _controller().get(solicitud_id)


@solicitudes_compra_bp.route("", methods=["GET"])
@solicitudes_compra_bp.arguments(ListarSolicitudesCompraSchema, location="query")
@solicitudes_compra_bp.doc(responses={200: {"description": "Listado de solicitudes de compra"}})
@require_auth
def list_solicitudes(filters):
    """Lista solicitudes de compra con filtros opcionales"""
    return _controller().list(filters)