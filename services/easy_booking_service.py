"""
EasyBookingService - Funcionalidade 3: Reserva Fácil

Concito: Processo de reserva simplificado
Propósito: Experiência de reserva rápida e intuitiva
"""
from domain.timeslot import TimeSlot
from domain.booking import Booking
from services.base import BaseService
import hashlib


class EasyBookingService(BaseService):
    """Serviço de reserva fácil"""

    def __init__(self):
        super().__init__("EasyBookingService")

    def selecionar_horario(self, slot: TimeSlot) -> TimeSlot:
        """
        Seleciona um período de tempo para reserva

        Args:
            slot: Período de tempo a selecionar

        Returns:
            Período selecionado
        """
        if slot.status != "DISPONIVEL":
            raise ValueError(f"Período não está disponível: {slot.status}")

        self.log(f"Período selecionado: {slot.id} ({slot.duracao_horas()} horas)")
        return slot

    def criar_reserva_rapida(
        self,
        user_id: str,
        space_id: str,
        slot_id: str,
        valor_total: float
    ) -> Booking:
        """
        Criação de reserva rápida

        Args:
            user_id: ID do usuário
            space_id: ID do espaço
            slot_id: ID do período de tempo
            valor_total: Preço total

        Returns:
            Reserva criada
        """
        self.validar_string(user_id, "ID do usuário")
        self.validar_string(space_id, "ID do espaço")
        self.validar_string(slot_id, "ID do período")
        self.validar_numero(valor_total, "Valor total", 0)

        booking_id = self._gerar_id_reserva(user_id, space_id, slot_id)
        booking = Booking(
            booking_id,
            user_id,
            space_id,
            slot_id,
            "RESERVADO",
            valor_total
        )

        self.log(f"Reserva rápida criada: {booking_id}")
        return booking

    def confirmar_reserva(self, booking: Booking) -> Booking:
        """Confirma reserva"""
        booking.confirmar()
        self.log(f"Reserva confirmada: {booking.id}")
        return booking

    def _gerar_id_reserva(self, user_id: str, space_id: str, slot_id: str) -> str:
        """Gera ID de reserva único"""
        combined = f"{user_id}_{space_id}_{slot_id}"
        hash_obj = hashlib.md5(combined.encode())
        return f"bk_{hash_obj.hexdigest()[:8]}"
