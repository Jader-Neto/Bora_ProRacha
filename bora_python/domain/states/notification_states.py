"""
Estados da Notification — Padrão State

Cada classe representa um estado concreto do ciclo de vida de uma notificação.

Ciclo de vida:
  PENDENTE → ENVIADA → LIDA
     ↓          ↓
   FALHA      FALHA
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from domain.notification import Notification


class EstadoNotification(ABC):
    """Interface base para todos os estados de uma notificação."""

    @abstractmethod
    def marcar_enviada(self, notification: "Notification") -> None: ...

    @abstractmethod
    def marcar_lida(self, notification: "Notification") -> None: ...

    @abstractmethod
    def marcar_falha(self, notification: "Notification") -> None: ...

    @property
    @abstractmethod
    def nome(self) -> str: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


# ─────────────────────────────────────────────
# Estados concretos
# ─────────────────────────────────────────────

class EstadoPendente(EstadoNotification):
    """Notificação criada, aguardando envio."""

    nome = "PENDENTE"

    def marcar_enviada(self, notification: "Notification") -> None:
        notification.data_envio = datetime.now()
        notification._set_estado(EstadoEnviada())

    def marcar_lida(self, notification: "Notification") -> None:
        # Permite marcar como lida direto do estado pendente (ex: push in-app)
        notification._set_estado(EstadoLida())

    def marcar_falha(self, notification: "Notification") -> None:
        notification._set_estado(EstadoFalha())


class EstadoEnviada(EstadoNotification):
    """Notificação entregue ao destinatário."""

    nome = "ENVIADA"

    def marcar_enviada(self, notification: "Notification") -> None:
        raise ValueError("Notificação já foi enviada")

    def marcar_lida(self, notification: "Notification") -> None:
        notification._set_estado(EstadoLida())

    def marcar_falha(self, notification: "Notification") -> None:
        notification._set_estado(EstadoFalha())


class EstadoLida(EstadoNotification):
    """Usuário visualizou a notificação — estado terminal positivo."""

    nome = "LIDA"

    def marcar_enviada(self, notification: "Notification") -> None:
        raise ValueError("Notificação já foi lida")

    def marcar_lida(self, notification: "Notification") -> None:
        raise ValueError("Notificação já está marcada como lida")

    def marcar_falha(self, notification: "Notification") -> None:
        raise ValueError("Não é possível marcar falha em notificação já lida")


class EstadoFalha(EstadoNotification):
    """Falha no envio — pode ser reenviada."""

    nome = "FALHA"

    def marcar_enviada(self, notification: "Notification") -> None:
        # Permite reenvio após falha
        notification.data_envio = datetime.now()
        notification._set_estado(EstadoEnviada())

    def marcar_lida(self, notification: "Notification") -> None:
        raise ValueError("Não é possível marcar como lida uma notificação com falha")

    def marcar_falha(self, notification: "Notification") -> None:
        raise ValueError("Notificação já está com status de falha")


# Mapeamento nome → instância (útil para reconstituir estado a partir do banco)
ESTADOS_NOTIFICATION: dict[str, EstadoNotification] = {
    "PENDENTE": EstadoPendente(),
    "ENVIADA": EstadoEnviada(),
    "LIDA": EstadoLida(),
    "FALHA": EstadoFalha(),
}
