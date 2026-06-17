"""
BaseRepository - Implementação genérica de repositório com operações CRUD
"""
from typing import List, Optional, TypeVar, Dict

from domain.base import BaseEntity

T = TypeVar('T', bound=BaseEntity)


class BaseRepository:
    """Repositório genérico com operações CRUD"""

    def __init__(self):
        self._items: Dict[str, BaseEntity] = {}

    def find_all(self) -> List[BaseEntity]:
        """Obtém todos os itens"""
        return list(self._items.values())

    def find_by_id(self, item_id: str) -> Optional[BaseEntity]:
        """Obtém item por ID"""
        return self._items.get(item_id)

    def save(self, entity: BaseEntity) -> BaseEntity:
        """Salva novo item"""
        if entity.id in self._items:
            raise ValueError(f"Entity with id {entity.id} already exists")
        self._items[entity.id] = entity
        return entity

    def update(self, item_id: str, entity: BaseEntity) -> Optional[BaseEntity]:
        """Atualiza item"""
        if item_id not in self._items:
            return None
        self._items[item_id] = entity
        return entity

    def delete(self, item_id: str) -> bool:
        """Deleta item"""
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True

    def count(self) -> int:
        """Conta itens"""
        return len(self._items)

    def clear(self) -> None:
        """Limpa todos os itens"""
        self._items.clear()
