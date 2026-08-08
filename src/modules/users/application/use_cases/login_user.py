# src/modules/users/application/use_cases/login_user.py
from dataclasses import dataclass
from src.modules.users.domain.repositories import UserRepository
from src.modules.users.domain.exceptions import InvalidCredentialsException
from src.shared.auth.strategies.base import AuthStrategy
from src.shared.auth.password_hasher import PasswordHasher  # ej. bcrypt wrapper


@dataclass
class LoginInput:
    correo: str
    password: str

@dataclass
class LoginOutput:
    access_token: str
    user_id: str
    correo: str


class LoginUseCase:
    def __init__(self, user_repository: UserRepository, auth_strategy: AuthStrategy, password_hasher: PasswordHasher):
        self._user_repository = user_repository
        self._auth_strategy = auth_strategy
        self.password_hasher = password_hasher

    def execute(self, data: LoginInput) -> LoginOutput:
        user = self._user_repository.get_by_correo(data.correo)
        if user is None or not self.password_hasher.verify(data.password, user.password):
            raise InvalidCredentialsException()
        token = self._auth_strategy.generate_token({
            "sub": str(user.id),
            "correo": user.correo,
        })

        return LoginOutput(access_token=token, user_id=str(user.id), correo=user.correo)