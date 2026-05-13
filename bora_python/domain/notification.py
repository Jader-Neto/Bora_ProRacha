"""
Notificação - Entidade representando notificações do sistema
"""
from datetime import datetime
from typing import Literal

from .base import EntityComStatus

NotificationStatus = Literal["PENDENTE", "ENVIADA", "LIDA", "FALHA"]
NotificationType = Literal["EMAIL", "SMS", "PUSH", "REMINDER"]


class Notification(EntityComStatus):
    """
    Entidade de notificação para rastreamento de notificações do sistema.
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

    def marcar_enviada(self) -> None:
        """Marcar notificação como enviada"""
        if self.status != "PENDENTE":
            raise ValueError(f"Não pode marcar notificação {self.status} como enviada")
        self.status = "ENVIADA"
        self.data_envio = datetime.now()

    def marcar_lida(self) -> None:
        """Marcar notificação como lida"""
        if self.status not in ["ENVIADA", "PENDENTE"]:
            raise ValueError(f"Não pode marcar notificação {self.status} como lida")
        self.status = "LIDA"

    def marcar_falha(self) -> None:
        """Marcar notificação como falha"""
        if self.status in ["LIDA", "FALHA"]:
            raise ValueError(f"Não pode marcar notificação {self.status} como falha")
        self.status = "FALHA"

    def __repr__(self):
        return (f"Notification(id={self.id}, user_id={self.user_id}, "
                f"tipo={self.tipo}, status={self.status})")
