"""
Intervalo de Tempo - Entidade representando um intervalo de tempo para reserva
"""
from datetime import datetime
from typing import Literal

from .base import EntityComStatus

SlotStatus = Literal["DISPONIVEL", "RESERVADO", "BLOQUEADO"]


class TimeSlot(EntityComStatus):
    """
    Entidade de intervalo de tempo para disponibilidade de reserva.
    """
    def __init__(
        self,
        slot_id: str,
        space_id: str,
        inicio: datetime,
        fim: datetime,
        status: SlotStatus = "DISPONIVEL"
    ):
        super().__init__(slot_id, status)
        self.space_id = space_id
        self.inicio = inicio
        self.fim = fim
        self._validar()

    def _validar(self) -> None:
        """Validar dados do intervalo"""
        if self.fim <= self.inicio:
            raise ValueError("Hora de fim deve ser após a hora de início")

    def duracao_horas(self) -> float:
        """Obter duração em horas"""
        delta = self.fim - self.inicio
        return delta.total_seconds() / 3600

    def reservar(self) -> None:
        """Reservar intervalo"""
        if self.status != "DISPONIVEL":
            raise ValueError(f"Não pode reservar intervalo com status {self.status}")
        self.status = "RESERVADO"

    def liberar(self) -> None:
        """Liberar intervalo"""
        if self.status == "BLOQUEADO":
            raise ValueError("Não pode liberar um intervalo bloqueado")
        self.status = "DISPONIVEL"

    def bloquear(self) -> None:
        """Bloquear intervalo"""
        self.status = "BLOQUEADO"

    def cancelar(self) -> None:
        """Cancelar intervalo (torná-lo disponível)"""
        if self.status != "RESERVADO":
            raise ValueError("Apenas intervalos reservados podem ser cancelados")
        self.status = "DISPONIVEL"

    def esta_disponivel(self) -> bool:
        """Verificar se intervalo está disponível"""
        return self.status == "DISPONIVEL"

    def __repr__(self):
        return (f"TimeSlot(id={self.id}, space_id={self.space_id}, "
                f"inicio={self.inicio}, status={self.status})")
