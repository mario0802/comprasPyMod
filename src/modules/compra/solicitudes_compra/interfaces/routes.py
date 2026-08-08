from flask import Blueprint

from src.modules.compra.solicitudes_compra.interfaces.controllers import SolicitudCompraController
from src.config.container import container
from src.shared.auth.decorators import require_auth

solicitudes_compra_bp = Blueprint(
    "solicitudes_compra", __name__, url_prefix="/api/solicitudes-compra"
)


def _controller() -> SolicitudCompraController:
    return container.get_solicitud_compra_controller()


@solicitudes_compra_bp.route("", methods=["POST"])
@require_auth
def create_solicitud():
    return _controller().create()


@solicitudes_compra_bp.route("/<int:solicitud_id>", methods=["PATCH"])
@require_auth
def update_solicitud(solicitud_id: int):
    return _controller().update(solicitud_id)


@solicitudes_compra_bp.route("/<int:solicitud_id>", methods=["GET"])
@require_auth
def get_solicitud(solicitud_id: int):
    return _controller().get(solicitud_id)


@solicitudes_compra_bp.route("", methods=["GET"])
@require_auth
def list_solicitudes():
    return _controller().list()