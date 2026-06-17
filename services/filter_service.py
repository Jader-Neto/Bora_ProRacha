"""
FilterService - Funcionalidade 4: Filtragem Dinâmica

Concito: Filtragem flexível de espaços com múltiplos critérios
Propósito: Ajudar usuários a encontrar espaços ideais facilmente
"""
from typing import List

from domain.space import Space
from domain.filtro import FiltroEspaco, FiltroPorLocal, FiltroPorEsporte, FiltroPorPreco, FiltroCombinado
from services.base import BaseService


class FilterService(BaseService):
    """Serviço de filtragem de espaços"""

    def __init__(self):
        super().__init__("FilterService")

    def aplicar_filtro(self, spaces: List[Space], filtro: FiltroEspaco) -> List[Space]:
        """Aplica filtro único aos espaços"""
        resultado = filtro.aplicar(spaces)  # onde o polimorfismo acontece - cada filtro tem sua própria lógica de aplicação
        self.log(f"Filtro aplicado: {filtro.obter_criterio()} → {len(resultado)} espaços encontrados")
        return resultado

    def filtrar_por_local(self, spaces: List[Space], local: str) -> List[Space]:
        """Filtra espaços por localização"""
        self.validar_string(local, "Localização")
        return self.aplicar_filtro(spaces, FiltroPorLocal(local))

    def filtrar_por_esporte(self, spaces: List[Space], esporte: str) -> List[Space]:
        """Filtra espaços por esporte"""
        self.validar_string(esporte, "Esporte")
        return self.aplicar_filtro(spaces, FiltroPorEsporte(esporte))

    def filtrar_por_preco(self, spaces: List[Space], preco_maximo: float) -> List[Space]:
        """Filtra espaços por preço máximo"""
        self.validar_numero(preco_maximo, "Preço máximo", 1)
        return self.aplicar_filtro(spaces, FiltroPorPreco(preco_maximo))

    def filtrar_avancado(
        self,
        spaces: List[Space],
        local: str = None,
        esporte: str = None,
        preco_maximo: float = None
    ) -> List[Space]:
        """
        Filtragem avançada com múltiplos critérios

        Args:
            spaces: Lista de espaços
            local: Filtro de localização
            esporte: Filtro de esporte
            preco_maximo: Filtro de preço máximo

        Returns:
            Lista de espaços filtrada
        """
        filtros = []

        if local:
            filtros.append(FiltroPorLocal(local))
        if esporte:
            filtros.append(FiltroPorEsporte(esporte))
        if preco_maximo:
            filtros.append(FiltroPorPreco(preco_maximo))

        if not filtros:
            return spaces

        filtro_combinado = FiltroCombinado(filtros)
        return self.aplicar_filtro(spaces, filtro_combinado)

    def ordenar_por_preco(self, spaces: List[Space], decrescente: bool = False) -> List[Space]:
        """Ordena espaços por preço"""
        return sorted(spaces, key=lambda s: s.preco_hora, reverse=decrescente)

    def ordenar_por_avaliacao(self, spaces: List[Space]) -> List[Space]:
        """Ordena espaços por avaliação"""
        return sorted(
            spaces,
            key=lambda s: s.obter_media_avaliacoes(),
            reverse=True
        )
