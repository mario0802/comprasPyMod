from sqlalchemy import Column, BigInteger, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from src.config.database import Base
from src.shared.infrastructure.base_model import AuditMixin

class SolicitudCompraModel(Base, AuditMixin):
    __tablename__ = "solicitudes_compra"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    fecha_solicitud = Column(TIMESTAMP, server_default=func.current_timestamp())
    descripcion = Column(Text, nullable=True)
    monto = Column(DECIMAL(10, 2), nullable=True)
    estado = Column(String(20), nullable=False, index=True)
    aprobado_por = Column(Integer, nullable=True)
    fecha_aprobacion = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"<SolicitudCompraModel id={self.id} estado={self.estado}>"