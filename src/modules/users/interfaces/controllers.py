from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.get_user import GetUserUseCase
from src.modules.users.application.dto import CreateUserDTO
from src.modules.users.interfaces.schemas import UserResponseSchema
from src.shared.utils.response import success_response
from src.modules.users.application.use_cases.login_user import LoginUseCase, LoginInput


class UserController:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        get_user_use_case: GetUserUseCase,
    ):
        self.create_user_use_case = create_user_use_case
        self.get_user_use_case = get_user_use_case

    def create(self, data: dict):
        # data ya viene validado por CreateUserSchema (vía @users_bp.arguments)

        # TODO: reemplazar por el id del usuario autenticado (g.current_user.id)
        id_usuario_creador = data.pop("id_usuario_creador", 0)

        dto = CreateUserDTO(**data, id_usuario_creador=id_usuario_creador)
        result = self.create_user_use_case.execute(dto)

        return success_response(
            data=UserResponseSchema().dump(result),
            status_code=201,
        )

    def get(self, user_id: int):
        result = self.get_user_use_case.execute(user_id)

        return success_response(
            data=UserResponseSchema().dump(result),
            status_code=200,
        )


class AuthController:
    def __init__(self, login_use_case: LoginUseCase):
        self._login_use_case = login_use_case

    def login(self, data: dict):
        # data ya viene validado por LoginSchema (vía @users_bp.arguments)
        result = self._login_use_case.execute(LoginInput(**data))

        return success_response(
            data={
                "access_token": result.access_token,
                "user": {
                    "id": result.user_id,
                    "correo": result.correo,
                },
            },
            status_code=200,
        )