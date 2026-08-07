from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.shared.domain.base_entity import BaseEntity


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    id: Optional[int] = None
    nombre: str
    apellido: str
    correo: str
    nick: str
    password: str  # hash, nunca texto plano

    def __post_init__(self):
        if not self.correo or "@" not in self.correo:
            raise ValueError("Correo inválido")
        if not self.nick:
            raise ValueError("El nick es obligatorio")