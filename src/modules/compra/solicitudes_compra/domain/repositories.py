from abc import ABC, abstractmethod
from typing import Optional

from src.modules.compra.solicitudes_compra.domain.entities import SolicitudCompraEntity


class SolicitudCompraRepository(ABC):
    @abstractmethod
    def get_by_id(self, solicitud_id: int) -> Optional[SolicitudCompraEntity]:
        ...

    @abstractmethod
    def create(self, solicitud: SolicitudCompraEntity) -> SolicitudCompraEntity:
        ...

    @abstractmethod
    def update(self, solicitud: SolicitudCompraEntity) -> SolicitudCompraEntity:
        ...

    @abstractmethod
    def delete(self, solicitud_id: int) -> None:
        ...

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> list[SolicitudCompraEntity]:
        ...

    @abstractmethod
    def list_by_solicitante(
        self, solicitante_id: int, limit: int = 100, offset: int = 0
    ) -> list[SolicitudCompraEntity]:
        ...

    @abstractmethod
    def list_by_estado(
        self, estado: str, limit: int = 100, offset: int = 0
    ) -> list[SolicitudCompraEntity]:
        ...