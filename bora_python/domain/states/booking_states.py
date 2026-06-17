"""
Estados do Booking — Padrão State

Cada classe representa um estado concreto do ciclo de vida de uma reserva.
O Booking delega todas as transições para o estado atual, eliminando
os blocos if/elif que existiam dentro de cada método.

Ciclo de vida:
  RESERVADO → CONFIRMADO → CHECKIN_REALIZADO → (fim)
       ↓            ↓               ↓
   CANCELADO   CANCELADO     NAO_COMPARECEU
       ↓
  REEMBOLSADO
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.booking import Booking


class EstadoBooking(ABC):
    """Interface base para todos os estados de uma reserva."""

    @abstractmethod
    def confirmar(self, booking: "Booking") -> None: ...

    @abstractmethod
    def cancelar(self, booking: "Booking", taxa: float) -> None: ...

    @abstractmethod
    def realizar_checkin(self, booking: "Booking") -> None: ...

    @abstractmethod
    def marcar_nao_comparecimento(self, booking: "Booking") -> None: ...

    @abstractmethod
    def reembolsar(self, booking: "Booking") -> None: ...

    @property
    @abstractmethod
    def nome(self) -> str: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


# ─────────────────────────────────────────────
# Estados concretos
# ─────────────────────────────────────────────

class EstadoReservado(EstadoBooking):
    """Reserva criada, aguardando confirmação de pagamento."""

    nome = "RESERVADO"

    def confirmar(self, booking: "Booking") -> None:
        booking._set_estado(EstadoConfirmado())

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        booking._taxa_cancelamento = taxa
        booking._set_estado(EstadoCancelado())

    def realizar_checkin(self, booking: "Booking") -> None:
        raise ValueError("Confirme a reserva antes de realizar o check-in")

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        raise ValueError("Reserva ainda não foi confirmada")

    def reembolsar(self, booking: "Booking") -> None:
        raise ValueError("Apenas reservas canceladas podem ser reembolsadas")


class EstadoConfirmado(EstadoBooking):
    """Pagamento confirmado — reserva ativa."""

    nome = "CONFIRMADO"

    def confirmar(self, booking: "Booking") -> None:
        raise ValueError("Reserva já está confirmada")

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        booking._taxa_cancelamento = taxa
        booking._set_estado(EstadoCancelado())

    def realizar_checkin(self, booking: "Booking") -> None:
        booking._set_estado(EstadoCheckinRealizado())

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        booking._set_estado(EstadoNaoCompareceu())

    def reembolsar(self, booking: "Booking") -> None:
        raise ValueError("Apenas reservas canceladas podem ser reembolsadas")


class EstadoCheckinRealizado(EstadoBooking):
    """Usuário fez check-in no espaço."""

    nome = "CHECKIN_REALIZADO"

    def confirmar(self, booking: "Booking") -> None:
        raise ValueError("Reserva já realizou check-in")

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        raise ValueError("Não é possível cancelar após o check-in")

    def realizar_checkin(self, booking: "Booking") -> None:
        raise ValueError("Check-in já foi realizado")

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        raise ValueError("Usuário já realizou check-in")

    def reembolsar(self, booking: "Booking") -> None:
        raise ValueError("Apenas reservas canceladas podem ser reembolsadas")


class EstadoCancelado(EstadoBooking):
    """Reserva cancelada pelo usuário ou sistema."""

    nome = "CANCELADO"

    def confirmar(self, booking: "Booking") -> None:
        raise ValueError("Não é possível confirmar uma reserva cancelada")

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        raise ValueError("Reserva já está cancelada")

    def realizar_checkin(self, booking: "Booking") -> None:
        raise ValueError("Não é possível fazer check-in em reserva cancelada")

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        raise ValueError("Reserva cancelada não pode ser marcada como não comparecimento")

    def reembolsar(self, booking: "Booking") -> None:
        booking._set_estado(EstadoReembolsado())


class EstadoNaoCompareceu(EstadoBooking):
    """Usuário não apareceu no horário reservado."""

    nome = "NAO_COMPARECEU"

    def confirmar(self, booking: "Booking") -> None:
        raise ValueError("Reserva encerrada por não comparecimento")

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        raise ValueError("Não é possível cancelar após não comparecimento")

    def realizar_checkin(self, booking: "Booking") -> None:
        raise ValueError("Não é possível fazer check-in após não comparecimento")

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        raise ValueError("Não comparecimento já foi registrado")

    def reembolsar(self, booking: "Booking") -> None:
        raise ValueError("Apenas reservas canceladas podem ser reembolsadas")


class EstadoReembolsado(EstadoBooking):
    """Reembolso processado — estado terminal."""

    nome = "REEMBOLSADO"

    def confirmar(self, booking: "Booking") -> None:
        raise ValueError("Reserva já foi reembolsada")

    def cancelar(self, booking: "Booking", taxa: float) -> None:
        raise ValueError("Reserva já foi reembolsada")

    def realizar_checkin(self, booking: "Booking") -> None:
        raise ValueError("Reserva já foi reembolsada")

    def marcar_nao_comparecimento(self, booking: "Booking") -> None:
        raise ValueError("Reserva já foi reembolsada")

    def reembolsar(self, booking: "Booking") -> None:
        raise ValueError("Reembolso já foi processado")


# Mapeamento nome → classe (útil para reconstituir estado a partir do banco)
ESTADOS_BOOKING: dict[str, EstadoBooking] = {
    "RESERVADO": EstadoReservado(),
    "CONFIRMADO": EstadoConfirmado(),
    "CHECKIN_REALIZADO": EstadoCheckinRealizado(),
    "CANCELADO": EstadoCancelado(),
    "NAO_COMPARECEU": EstadoNaoCompareceu(),
    "REEMBOLSADO": EstadoReembolsado(),
}
