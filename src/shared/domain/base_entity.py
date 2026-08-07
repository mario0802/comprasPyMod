from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class BaseEntity:
    id_usuario_creador: int
    id_usuario_modificador: Optional[int] = None
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_modificacion: Optional[datetime] = None

    def marcar_modificacion(self, id_usuario_modificador: int) -> None:
        """Actualiza los campos de auditoría al modificar la entidad."""
        self.id_usuario_modificador = id_usuario_modificador
        self.fecha_modificacion = datetime.utcnow()