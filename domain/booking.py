"""
Booking — Entidade representando uma reserva de espaço

Padrão State aplicado: os métodos de transição (confirmar, cancelar,
realizar_checkin, marcar_nao_comparecimento, reembolsar) delegam para
o estado atual em vez de conter blocos if/elif internos.
Isso torna cada regra de transição isolada, testável e extensível.
"""
from datetime import datetime
from typing import Literal

from .base import EntityComStatus
from .states.booking_states import (
    EstadoBooking,
    EstadoReservado,
    ESTADOS_BOOKING,
)

BookingStatus = Literal[
    "RESERVADO", "CONFIRMADO", "CANCELADO",
    "CHECKIN_REALIZADO", "NAO_COMPARECEU", "REEMBOLSADO"
]


class Booking(EntityComStatus):
    """
    Entidade de reserva com lógica financeira e encapsulamento.
    O ciclo de vida é controlado pelo padrão State.
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

        # Inicializa o estado a partir do status recebido
        self._estado: EstadoBooking = ESTADOS_BOOKING.get(status, EstadoReservado())

        self._validar()

    def _validar(self) -> None:
        if self._valor_total < 0:
            raise ValueError("Valor total não pode ser negativo")
        if self._taxa_cancelamento < 0:
            raise ValueError("Taxa de cancelamento não pode ser negativa")

    # ── Método interno usado pelos estados para trocar estado ──────────────
    def _set_estado(self, novo_estado: EstadoBooking) -> None:
        self._estado = novo_estado
        self.status = novo_estado.nome

    # ── Propriedades ───────────────────────────────────────────────────────
    @property
    def valor_total(self) -> float:
        return self._valor_total

    @property
    def taxa_cancelamento(self) -> float:
        return self._taxa_cancelamento

    @property
    def reembolso(self) -> float:
        return max(0, self._valor_total - self._taxa_cancelamento)

    @property
    def data_reserva(self) -> datetime:
        return self._data_reserva

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

    # ── Transições — delegadas ao estado atual ─────────────────────────────
    def confirmar(self) -> None:
        """Confirmar reserva (RESERVADO → CONFIRMADO)"""
        self._estado.confirmar(self)

    def cancelar(self, taxa: float = 0.0) -> None:
        """Cancelar reserva (RESERVADO|CONFIRMADO → CANCELADO)"""
        if taxa < 0:
            raise ValueError("Taxa de cancelamento não pode ser negativa")
        self._estado.cancelar(self, taxa)

    def realizar_checkin(self) -> None:
        """Realizar check-in (CONFIRMADO → CHECKIN_REALIZADO)"""
        self._estado.realizar_checkin(self)

    def marcar_nao_comparecimento(self) -> None:
        """Marcar não comparecimento (CONFIRMADO → NAO_COMPARECEU)"""
        self._estado.marcar_nao_comparecimento(self)

    def reembolsar(self) -> None:
        """Processar reembolso (CANCELADO → REEMBOLSADO)"""
        self._estado.reembolsar(self)

    def __repr__(self):
        return (
            f"Booking(id={self.id}, user_id={self.user_id}, "
            f"space_id={self.space_id}, status={self.status}, "
            f"valor={self._valor_total})"
        )
