"""
Interfaces para Polimorfismo - Contratos base para serviços e entidades
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class INotificador(ABC):
    """
    Interface para serviço de notificação.
    Permite diferentes implementações (Email, SMS, Push, etc)
    """
    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        """Enviar notificação"""
        pass

    @abstractmethod
    def confirmar(self, notif_id: str) -> bool:
        """Confirmar notificação"""
        pass

    @abstractmethod
    def obter_status(self, notif_id: str) -> str:
        """Obter status da notificação"""
        pass


class IRepository(ABC, Generic[T]):
    """
    Interface para repositório (operações CRUD).
    Garante consistência nas operações de dados.
    """
    @abstractmethod
    def find_all(self) -> List[T]:
        """Obter todos os itens"""
        pass

    @abstractmethod
    def find_by_id(self, item_id: str) -> Optional[T]:
        """Obter item por ID"""
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        """Salvar novo item"""
        pass

    @abstractmethod
    def update(self, item_id: str, entity: T) -> Optional[T]:
        """Atualizar item"""
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Deletar item"""
        pass

    @abstractmethod
    def count(self) -> int:
        """Contar itens"""
        pass


class IFiltro(ABC, Generic[T]):
    """
    Interface para serviço de filtro.
    Permite diferentes estratégias de filtro.
    """
    @abstractmethod
    def aplicar(self, items: List[T]) -> List[T]:
        """Aplicar filtro"""
        pass

    @abstractmethod
    def obter_criterio(self) -> str:
        """Obter descrição de critério do filtro"""
        pass


class ICalculadora(ABC):
    """
    Interface para cálculo de preço e taxa.
    Permite diferentes estratégias de cálculo.
    """
    @abstractmethod
    def calcular(self, valor: float) -> float:
        """Calcular valor"""
        pass

    @abstractmethod
    def obter_descricao(self) -> str:
        """Obter descrição do cálculo"""
        pass


class IProcessadorReserva(ABC):
    """
    Interface para processamento de reserva.
    Permite diferentes fluxos de reserva.
    """
    @abstractmethod
    def processar(self) -> None:
        """Processar reserva"""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Validar reserva"""
        pass

    @abstractmethod
    def executar(self) -> None:
        """Executar reserva"""
        pass

    @abstractmethod
    def reverter(self) -> None:
        """Reverter reserva"""
        pass


class IGerenciadorEstado(ABC, Generic[T]):
    """
    Interface para gerenciamento de estado.
    Permite diferentes máquinas de estado.
    """
    @abstractmethod
    def obter_estado(self) -> T:
        """Obter estado atual"""
        pass

    @abstractmethod
    def transicionar(self, novo_estado: T) -> None:
        """Transicionar para novo estado"""
        pass

    @abstractmethod
    def validar_transicao(self, novo_estado: T) -> bool:
        """Validar transição de estado"""
        pass
