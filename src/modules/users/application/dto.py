from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateUserDTO:
    """Datos de entrada para crear un usuario."""
    nombre: str
    apellido: str
    correo: str
    nick: str
    password: str  # texto plano, se hashea en el use case
    id_usuario_creador: int


@dataclass
class UserResponseDTO:
    """Datos de salida — nunca incluye password."""
    id: int
    nombre: str
    apellido: str
    correo: str
    nick: str
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime]

    @staticmethod
    def from_entity(entity) -> "UserResponseDTO":
        return UserResponseDTO(
            id=entity.id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            correo=entity.correo,
            nick=entity.nick,
            fecha_creacion=entity.fecha_creacion,
            fecha_modificacion=entity.fecha_modificacion,
        )