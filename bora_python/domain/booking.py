"""
Reserva - Entidade representando uma reserva de espaço
Com encapsulamento: atributos protegidos e lógica financeira
"""
from datetime import datetime
from typing import Literal

from .base import EntityComStatus

BookingStatus = Literal["RESERVADO", "CONFIRMADO", "CANCELADO", "CHECKIN_REALIZADO", 
                        "NAO_COMPARECEU", "REEMBOLSADO"]


class Booking(EntityComStatus):
    """
    Entidade de reserva com lógica financeira e encapsulamento.
    """
    def __init__(
        self,
        booking_id: str,
        user_id: str,
        space_id: str,
        slot_id: str,
        status: BookingStatus = "RESERVADO",
        valor_total: float = 0.0,
        taxa_cancelamento: float = 0.0
    ):
        super().__init__(booking_id, status)
        self.user_id = user_id
        self.space_id = space_id
        self.slot_id = slot_id
        self._valor_total = valor_total
        self._taxa_cancelamento = taxa_cancelamento
        self._data_reserva = datetime.now()
        self._validar()

    def _validar(self) -> None:
        """Validar dados da reserva"""
        if self._valor_total < 0:
            raise ValueError("Valor total não pode ser negativo")
        if self._taxa_cancelamento < 0:
            raise ValueError("Taxa de cancelamento não pode ser negativa")

    # Propriedades
    @property
    def valor_total(self) -> float:
        return self._valor_total

    @property
    def taxa_cancelamento(self) -> float:
        return self._taxa_cancelamento

    @property
    def reembolso(self) -> float:
        """Calcular valor do reembolso"""
        return max(0, self._valor_total - self._taxa_cancelamento)

    @property
    def data_reserva(self) -> datetime:
        return self._data_reserva

    # Modificadores
    @valor_total.setter
    def valor_total(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("Valor não pode ser negativo")
        self._valor_total = valor

    @taxa_cancelamento.setter
    def taxa_cancelamento(self, taxa: float) -> None:
        if taxa < 0:
            raise ValueError("Taxa de cancelamento não pode ser negativa")
        self._taxa_cancelamento = taxa

    # Métodos de negócio
    def confirmar(self) -> None:
        """Confirmar reserva"""
        if self.status != "RESERVADO":
            raise ValueError("Apenas reservas podem ser confirmadas")
        self.status = "CONFIRMADO"

    def cancelar(self, taxa: float = 0.0) -> None:
        """Cancelar reserva"""
        if taxa < 0:
            raise ValueError("Taxa de cancelamento não pode ser negativa")
        if self.status in ["CANCELADO", "NAO_COMPARECEU"]:
            raise ValueError(f"Não pode cancelar reserva com status {self.status}")
        self._taxa_cancelamento = taxa
        self.status = "CANCELADO"

    def realizar_checkin(self) -> None:
        """Realizar check-in"""
        if self.status != "CONFIRMADO":
            raise ValueError("Apenas reservas confirmadas podem fazer check-in")
        self.status = "CHECKIN_REALIZADO"

    def marcar_nao_comparecimento(self) -> None:
        """Marcar como não comparecimento"""
        if self.status not in ["CONFIRMADO", "CHECKIN_REALIZADO"]:
            raise ValueError("Apenas reservas confirmadas podem ser marcadas como não comparecimento")
        self.status = "NAO_COMPARECEU"

    def reembolsar(self) -> None:
        """Process refund"""
        if self.status != "CANCELADO":
            raise ValueError("Only cancelled bookings can be refunded")
        self.status = "REEMBOLSADO"

    def __repr__(self):
        return (f"Booking(id={self.id}, user_id={self.user_id}, space_id={self.space_id}, "
                f"status={self.status}, valor={self._valor_total})")
