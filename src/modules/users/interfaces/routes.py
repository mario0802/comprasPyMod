from flask import Blueprint

from src.modules.users.interfaces.controllers import UserController
from src.config.container import container

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def _controller() -> UserController:
    return container.get_user_controller()


@users_bp.route("", methods=["POST"])
def create_user():
    return _controller().create()


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    return _controller().get(user_id)