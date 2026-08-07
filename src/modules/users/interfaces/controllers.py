from flask import request

from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.get_user import GetUserUseCase
from src.modules.users.application.dto import CreateUserDTO
from src.modules.users.interfaces.schemas import CreateUserSchema, UserResponseSchema
from src.shared.utils.response import success_response


class UserController:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        get_user_use_case: GetUserUseCase,
    ):
        self.create_user_use_case = create_user_use_case
        self.get_user_use_case = get_user_use_case

    def create(self):
        data = CreateUserSchema().load(request.get_json())

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