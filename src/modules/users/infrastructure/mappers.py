from src.modules.users.domain.entities import UserEntity
from src.modules.users.infrastructure.models import UserModel


class UserMapper:
    """Traduce entre UserModel (infraestructura/Postgres) y UserEntity (dominio)."""

    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            nombre=model.nombre,
            apellido=model.apellido,
            correo=model.correo,
            nick=model.nick,
            password=model.password,
            id_usuario_creador=model.id_usuario_creador,
            fecha_creacion=model.fecha_creacion,
            id_usuario_modificador=model.id_usuario_modificador,
            fecha_modificacion=model.fecha_modificacion,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            correo=entity.correo,
            nick=entity.nick,
            password=entity.password,
            id_usuario_creador=entity.id_usuario_creador,
            fecha_creacion=entity.fecha_creacion,
            id_usuario_modificador=entity.id_usuario_modificador,
            fecha_modificacion=entity.fecha_modificacion,
        )