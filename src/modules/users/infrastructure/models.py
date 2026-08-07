from sqlalchemy import Column, BigInteger, String
from src.config.database import Base
from src.shared.infrastructure.base_model import AuditMixin


class UserModel(Base, AuditMixin):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True, index=True)
    nick = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<UserModel id={self.id} nick={self.nick}>"