"""
ReminderService - Funcionalidade 7: Lembretes Interativos

Concito: Enviar lembretes para reservas próximas
Propósito: Reduzir não comparecimento e melhorar engajamento do usuário
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from domain.booking import Booking
from domain.notification import Notification
from services.base import BaseService
import uuid


class ReminderService(BaseService):
    """Serviço para lembretes de reservas"""

    def __init__(self):
        super().__init__("ReminderService")
        self._lembretes: Dict[str, Notification] = {}

    def agendar_lembrete(self, booking: Booking, horas_antes: int = 24) -> Notification:
        """
        Agenda lembrete para reserva

        Args:
            booking: Objeto de reserva
            horas_antes: Horas antes da reserva para lembrar (padrão 24)

        Returns:
            Objeto de notificação
        """
        if horas_antes < 0:
            raise ValueError("As horas devem ser positivas")

        lembrete_id = f"rem_{uuid.uuid4().hex[:8]}"

        notificacao = Notification(
            lembrete_id,
            booking.user_id,
            "Lembrete de Reserva",
            f"Sua reserva está agendada para em {horas_antes} horas. Não esqueça!",
            "REMINDER",
            "PENDENTE"
        )

        self._lembretes[lembrete_id] = notificacao
        self.log(f"Lembrete agendado para a reserva {booking.id}")

        return notificacao

    def obter_lembretes_pendentes(self) -> List[Notification]:
        """Obtém todos os lembretes pendentes"""
        return [n for n in self._lembretes.values() if n.status == "PENDENTE"]

    def enviar_lembrete(self, lembrete_id: str) -> bool:
        """Envia notificação de lembrete"""
        if lembrete_id not in self._lembretes:
            return False

        notificacao = self._lembretes[lembrete_id]
        notificacao.marcar_enviada()
        self.log(f"Lembrete enviado: {lembrete_id}")

        return True

    def enviar_todos_lembretes(self) -> int:
        """Envia todos os lembretes pendentes"""
        lembretes_pendentes = self.obter_lembretes_pendentes()
        enviados = 0

        for lembrete in lembretes_pendentes:
            if self.enviar_lembrete(lembrete.id):
                enviados += 1

        self.log(f"Total de lembretes enviados: {enviados}")
        return enviados

    def obter_historico_lembretes(self, user_id: str) -> List[Notification]:
        """Obtém histórico de lembretes para o usuário"""
        return [n for n in self._lembretes.values() if n.user_id == user_id]

    def cancelar_lembrete(self, lembrete_id: str) -> bool:
        """Cancela lembrete agendado"""
        if lembrete_id not in self._lembretes:
            return False

        notificacao = self._lembretes[lembrete_id]
        if notificacao.status == "PENDENTE":
            del self._lembretes[lembrete_id]
            self.log(f"Lembrete cancelado: {lembrete_id}")
            return True

        return False

    def obter_estatisticas_lembretes(self) -> Dict:
        """Obtém estatísticas de lembretes"""
        lembretes = list(self._lembretes.values())

        stats = {
            "total": len(lembretes),
            "pendentes": len([n for n in lembretes if n.status == "PENDENTE"]),
            "enviadas": len([n for n in lembretes if n.status == "ENVIADA"]),
            "lidas": len([n for n in lembretes if n.status == "LIDA"]),
            "falhas": len([n for n in lembretes if n.status == "FALHA"])
        }

        return stats
