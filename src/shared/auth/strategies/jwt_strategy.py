# src/shared/auth/strategies/jwt_strategy.py
import jwt
import datetime
from typing import Any, Dict

from src.shared.auth.strategies.base import AuthStrategy
from src.shared.exceptions.base import UnauthorizedException


class JWTAuthStrategy(AuthStrategy):
    def __init__(self, secret_key: str, algorithm: str = "HS256",
                 expires_in_minutes: int = 60):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_in_minutes = expires_in_minutes

    def generate_token(self, payload: Dict[str, Any]) -> str:
        data = payload.copy()
        data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self._expires_in_minutes
        )
        data["iat"] = datetime.datetime.utcnow()
        return jwt.encode(data, self._secret_key, algorithm=self._algorithm)

    def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token expirado")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Token inválido")

    def refresh_token(self, token: str) -> str:
        payload = self.validate_token(token)
        payload.pop("exp", None)
        payload.pop("iat", None)
        return self.generate_token(payload)