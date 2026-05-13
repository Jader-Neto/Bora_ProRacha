"""
Estratégias de filtro para espaços - Implementa o padrão Strategy
"""
from abc import abstractmethod
from typing import List

from .interfaces import IFiltro
from .space import Space


class FiltroEspaco(IFiltro):
    """Classe base para filtros de espaços"""
    @abstractmethod
    def aplicar(self, espacos: List[Space]) -> List[Space]:
        pass

    @abstractmethod
    def obter_criterio(self) -> str:
        pass


class FiltroPorLocal(FiltroEspaco):
    """Filtro espaços por localização"""
    def __init__(self, localizacao: str):
        self.localizacao = localizacao

    def aplicar(self, espacos: List[Space]) -> List[Space]:
        return [e for e in espacos if e.localizacao.lower() == self.localizacao.lower()]

    def obter_criterio(self) -> str:
        return f"Location: {self.localizacao}"


class FiltroPorEsporte(FiltroEspaco):
    """Filtro espaços por esporte"""
    def __init__(self, esporte: str):
        self.esporte = esporte

    def aplicar(self, espacos: List[Space]) -> List[Space]:
        return [e for e in espacos if e.esporte.lower() == self.esporte.lower()]

    def obter_criterio(self) -> str:
        return f"Esporte: {self.esporte}"


class FiltroPorPreco(FiltroEspaco):
    """Filtro espaços por preço"""
    def __init__(self, preco_maximo: float):
        self.preco_maximo = preco_maximo

    def aplicar(self, espacos: List[Space]) -> List[Space]:
        return [e for e in espacos if e.preco_hora <= self.preco_maximo]

    def obter_criterio(self) -> str:
        return f"Preço máximo: R$ {self.preco_maximo}"


class FiltroPorStatus(FiltroEspaco):
    """Filtro espaços por status"""
    def __init__(self, status: str):
        self.status = status

    def aplicar(self, espacos: List[Space]) -> List[Space]:
        return [e for e in espacos if e.status == self.status]

    def obter_criterio(self) -> str:
        return f"Status: {self.status}"


class FiltroCombinado(FiltroEspaco):
    """Combinar múltiplos filtros - Padrão Composite"""
    def __init__(self, filtros: List[FiltroEspaco]):
        self.filtros = filtros

    def aplicar(self, espacos: List[Space]) -> List[Space]:
        resultado = espacos
        for filtro in self.filtros:
            resultado = filtro.aplicar(resultado)
        return resultado

    def obter_criterio(self) -> str:
        criterios = [f.obter_criterio() for f in self.filtros]
        return " AND ".join(criterios)
