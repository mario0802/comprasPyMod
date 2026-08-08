from flask import Blueprint

from src.modules.users.interfaces.controllers import UserController, AuthController
from src.config.container import container
from src.shared.auth.decorators import require_auth

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def _controller() -> UserController:
    return container.get_user_controller()

def _auth_controller() -> AuthController:
    return container.get_auth_controller()


@users_bp.route("", methods=["POST"])
def create_user():
    return _controller().create()


@users_bp.route("/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id: int):
    return _controller().get(user_id)

@users_bp.post("/login")
def login():
    return _auth_controller().login()