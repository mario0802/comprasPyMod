from abc import ABC, abstractmethod
from typing import Optional

from src.modules.users.domain.entities import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_by_nick(self, nick: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def delete(self, user_id: int) -> None:
        ...

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> list[UserEntity]:
        ...