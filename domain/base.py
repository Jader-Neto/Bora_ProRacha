"""
EntidadeBase e EntidadeComStatus - Classes base do sistema

Todas as entidades (Usuário, Reserva, Espaço, Intervalo de Tempo, Notificação) herdam dessas classes.
Isto garante que cada entidade tem um ID único e comportamento consistente.
"""
from abc import ABC
from typing import Any


class BaseEntity(ABC):
    """
    Classe base para todas as entidades do sistema.
    Cada entidade deve ter um ID único.
    """
    def __init__(self, entity_id: str):
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("ID da entidade deve ser uma string não vazia")
        self.id = entity_id

    def __eq__(self, other):
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class EntityComStatus(BaseEntity):
    """
    Classe base para entidades que gerenciam estados.
    
    Herda de EntidadeBase e adiciona funcionalidade de gerenciamento de status.
    Usada por: Reserva, Intervalo de Tempo, Notificação
    """
    def __init__(self, entity_id: str, status: str):
        super().__init__(entity_id)
        if not status or not isinstance(status, str):
            raise ValueError("Status deve ser uma string não vazia")
        self.status = status

    def validar_transicao(self, status_atual: str, status_permitidos: list[str]) -> None:
        """
        Valida se a transição de estado é permitida.
        
        Args:
            status_atual: Status atual
            status_permitidos: Lista de status permitidos para transição
            
        Raises:
            ValueError: Se a transição não for permitida
        """
        if status_atual not in status_permitidos:
            raise ValueError(f"Transição de estado inválida: {status_atual} não está em {status_permitidos}")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, status={self.status})"
