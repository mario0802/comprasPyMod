# src/shared/auth/strategies/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class AuthStrategy(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, Any]) -> str:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> Dict[str, Any]:
        """Debe lanzar InvalidTokenException si no es válido."""
        ...

    @abstractmethod
    def refresh_token(self, token: str) -> str:
        ...