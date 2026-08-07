from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Column
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class AuditMixin:
    """
    Mixin con los campos de auditoría estándar para
    todos los modelos SQLAlchemy (tablas Postgres).
    """

    @declared_attr
    def id_usuario_creador(cls):
        return Column(BigInteger, nullable=False)

    @declared_attr
    def fecha_creacion(cls):
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def id_usuario_modificador(cls):
        return Column(BigInteger, nullable=True)

    @declared_attr
    def fecha_modificacion(cls):
        return Column(
            DateTime,
            nullable=True,
            onupdate=datetime.utcnow
        )