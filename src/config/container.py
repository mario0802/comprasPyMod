from src.config.database import SessionLocal
from src.shared.auth.password_hasher import PasswordHasher
from src.config.settings import settings

from src.shared.auth.strategies.jwt_strategy import JWTAuthStrategy

from src.modules.users.infrastructure.repositories_impl import SQLAlchemyUserRepository
from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.get_user import GetUserUseCase
from src.modules.users.application.use_cases.login_user import LoginUseCase
from src.modules.users.interfaces.controllers import UserController, AuthController

class Container:
    @property
    def session(self):
        return SessionLocal()  # misma sesión durante todo el request

    @property
    def password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @property
    def auth_strategy(self) -> JWTAuthStrategy:
        return JWTAuthStrategy(
            secret_key=settings.JWT_SECRET_KEY,
            expires_in_minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN,
        )

    # ---------- USERS ----------
    @property
    def user_repository(self) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(self.session)

    def get_user_controller(self) -> UserController:
        return UserController(
            create_user_use_case=CreateUserUseCase(
                self.user_repository, self.password_hasher, self.session
            ),
            get_user_use_case=GetUserUseCase(self.user_repository),
        )

    # ---------- AUTH ----------
    def get_auth_controller(self) -> AuthController:
        return AuthController(
            login_use_case=LoginUseCase(
                self.user_repository, self.auth_strategy, self.password_hasher
            ),
        )

container = Container()