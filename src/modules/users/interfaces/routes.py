from flask_smorest import Blueprint

from src.modules.users.interfaces.controllers import UserController, AuthController
from src.modules.users.interfaces.schemas import (
    CreateUserSchema,
    UserResponseSchema,
    LoginSchema,
)
from src.config.container import container
from src.shared.auth.decorators import require_auth

users_bp = Blueprint(
    "users", __name__,
    url_prefix="/api/users",
    description="Operaciones sobre usuarios"
)


def _controller() -> UserController:
    return container.get_user_controller()


def _auth_controller() -> AuthController:
    return container.get_auth_controller()


@users_bp.route("", methods=["POST"])
@users_bp.arguments(CreateUserSchema)
@users_bp.doc(responses={201: {"description": "Usuario creado exitosamente"}})
def create_user(new_data):
    """Crea un nuevo usuario"""
    return _controller().create(new_data)


@users_bp.route("/<int:user_id>", methods=["GET"])
@users_bp.doc(responses={200: {"description": "Usuario encontrado"}})
@require_auth
def get_user(user_id: int):
    """Obtiene un usuario por id (requiere autenticación)"""
    return _controller().get(user_id)


@users_bp.route("/login", methods=["POST"])
@users_bp.arguments(LoginSchema)
@users_bp.doc(responses={200: {"description": "Login exitoso, retorna access_token"}})
def login(credentials):
    """Login de usuario, retorna JWT"""
    return _auth_controller().login(credentials)