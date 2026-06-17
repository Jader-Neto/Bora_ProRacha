"""
Notification — Entidade representando notificações do sistema

Padrão State aplicado: os métodos marcar_enviada, marcar_lida e
marcar_falha delegam para o estado atual, eliminando os if/elif
que verificavam o status antes de cada transição.
"""
from datetime import datetime
from typing import Literal

from .base import EntityComStatus
from .states.notification_states import (
    EstadoNotification,
    EstadoPendente,
    ESTADOS_NOTIFICATION,
)

NotificationStatus = Literal["PENDENTE", "ENVIADA", "LIDA", "FALHA"]
NotificationType = Literal["EMAIL", "SMS", "PUSH", "REMINDER"]


class Notification(EntityComStatus):
    """
    Entidade de notificação com ciclo de vida controlado pelo padrão State.
    """

    def __init__(
        self,
        notif_id: str,
        user_id: str,
        titulo: str,
        mensagem: str,
        tipo: NotificationType = "EMAIL",
        status: NotificationStatus = "PENDENTE"
    ):
        super().__init__(notif_id, status)
        self.user_id = user_id
        self.titulo = titulo
        self.mensagem = mensagem
        self.tipo = tipo
        self.data_criacao = datetime.now()
        self.data_envio: datetime | None = None

        # Inicializa estado a partir do status recebido
        self._estado: EstadoNotification = ESTADOS_NOTIFICATION.get(
            status, EstadoPendente()
        )

    # ── Método interno usado pelos estados para trocar estado ──────────────
    def _set_estado(self, novo_estado: EstadoNotification) -> None:
        self._estado = novo_estado
        self.status = novo_estado.nome

    # ── Transições — delegadas ao estado atual ─────────────────────────────
    def marcar_enviada(self) -> None:
        """Marcar como enviada (PENDENTE|FALHA → ENVIADA)"""
        self._estado.marcar_enviada(self)

    def marcar_lida(self) -> None:
        """Marcar como lida (PENDENTE|ENVIADA → LIDA)"""
        self._estado.marcar_lida(self)

    def marcar_falha(self) -> None:
        """Marcar como falha (PENDENTE|ENVIADA → FALHA)"""
        self._estado.marcar_falha(self)

    def __repr__(self):
        return (
            f"Notification(id={self.id}, user_id={self.user_id}, "
            f"tipo={self.tipo}, status={self.status})"
        )
