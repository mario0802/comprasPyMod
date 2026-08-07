from src.config.database import SessionLocal
from src.shared.auth.password_hasher import PasswordHasher

from src.modules.users.infrastructure.repositories_impl import SQLAlchemyUserRepository
from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.get_user import GetUserUseCase
from src.modules.users.interfaces.controllers import UserController

class Container:
    @property
    def session(self):
        return SessionLocal()  # misma sesión durante todo el request

    @property
    def password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    # ---------- USERS ----------
    @property
    def user_repository(self) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(self.session)

    def get_user_controller(self) -> UserController:
        return UserController(
            create_user_use_case=CreateUserUseCase(
                self.user_repository, self.password_hasher
            ),
            get_user_use_case=GetUserUseCase(self.user_repository),
        )

    # ---------- ORDERS (ejemplo futuro) ----------
    # @property
    # def order_repository(self):
    #     return SQLAlchemyOrderRepository(self.session)
    #
    # def get_order_controller(self):
    #     return OrderController(...)


container = Container()