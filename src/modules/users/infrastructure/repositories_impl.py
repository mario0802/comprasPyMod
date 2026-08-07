from typing import Optional

from sqlalchemy.orm import Session

from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import UserRepository
from src.modules.users.infrastructure.models import UserModel
from src.modules.users.infrastructure.mappers import UserMapper


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        model = self.session.query(UserModel).filter_by(id=user_id).first()
        return UserMapper.to_entity(model) if model else None

    def get_by_correo(self, correo: str) -> Optional[UserEntity]:
        model = self.session.query(UserModel).filter_by(correo=correo).first()
        return UserMapper.to_entity(model) if model else None

    def get_by_nick(self, nick: str) -> Optional[UserEntity]:
        model = self.session.query(UserModel).filter_by(nick=nick).first()
        return UserMapper.to_entity(model) if model else None

    def create(self, user: UserEntity) -> UserEntity:
        model = UserMapper.to_model(user)
        self.session.add(model)
        self.session.flush()  # para obtener el id generado sin hacer commit todavía
        return UserMapper.to_entity(model)

    def update(self, user: UserEntity) -> UserEntity:
        model = self.session.query(UserModel).filter_by(id=user.id).first()
        if model is None:
            raise ValueError(f"Usuario con id '{user.id}' no encontrado")

        model.nombre = user.nombre
        model.apellido = user.apellido
        model.correo = user.correo
        model.nick = user.nick
        model.password = user.password
        model.id_usuario_modificador = user.id_usuario_modificador
        model.fecha_modificacion = user.fecha_modificacion

        self.session.flush()
        return UserMapper.to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self.session.query(UserModel).filter_by(id=user_id).first()
        if model is None:
            raise ValueError(f"Usuario con id '{user_id}' no encontrado")
        self.session.delete(model)
        self.session.flush()

    def list_all(self, limit: int = 100, offset: int = 0) -> list[UserEntity]:
        models = self.session.query(UserModel).limit(limit).offset(offset).all()
        return [UserMapper.to_entity(m) for m in models]