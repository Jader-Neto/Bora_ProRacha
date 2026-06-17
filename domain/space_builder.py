"""
SpaceBuilder - Padrão Builder para criação de espaços esportivos

Propósito: Centralizar e simplificar a criação de objetos Space,
evitando construtores com muitos parâmetros posicionais e garantindo
validações antes da instanciação.
"""
from typing import List

from .space import Space


class SpaceBuilder:
    """
    Builder para criação fluente de espaços esportivos.

    Uso:
        space = (SpaceBuilder("s1", "Arena Pajuçara")
            .com_esporte("Futebol")
            .com_localizacao("Pajuçara, Maceió - AL")
            .com_preco(120.0)
            .com_fotos(["https://example.com/foto1.jpg"])
            .com_timezone("America/Sao_Paulo")
            .com_status("DISPONIVEL")
            .build())
    """

    def __init__(self, space_id: str, nome: str):
        if not space_id or not space_id.strip():
            raise ValueError("ID do espaço é obrigatório")
        if not nome or not nome.strip():
            raise ValueError("Nome do espaço é obrigatório")

        self._space_id = space_id
        self._nome = nome
        self._esporte: str | None = None
        self._localizacao: str | None = None
        self._preco_hora: float | None = None
        self._fotos: List[str] = []
        self._status: str = "DISPONIVEL"
        self._timezone: str = "America/Sao_Paulo"

    def com_esporte(self, esporte: str) -> "SpaceBuilder":
        """Define o tipo de esporte do espaço"""
        if not esporte or not esporte.strip():
            raise ValueError("Esporte não pode ser vazio")
        self._esporte = esporte
        return self

    def com_localizacao(self, localizacao: str) -> "SpaceBuilder":
        """Define a localização do espaço"""
        if not localizacao or not localizacao.strip():
            raise ValueError("Localização não pode ser vazia")
        self._localizacao = localizacao
        return self

    def com_preco(self, preco_hora: float) -> "SpaceBuilder":
        """Define o preço por hora"""
        if preco_hora <= 0:
            raise ValueError("Preço por hora deve ser maior que zero")
        self._preco_hora = preco_hora
        return self

    def com_fotos(self, fotos: List[str]) -> "SpaceBuilder":
        """Define a lista de URLs de fotos"""
        if not isinstance(fotos, list):
            raise ValueError("Fotos deve ser uma lista")
        self._fotos = fotos.copy()
        return self

    def com_foto(self, url: str) -> "SpaceBuilder":
        """Adiciona uma única foto à lista"""
        if url and url.strip():
            self._fotos.append(url)
        return self

    def com_status(self, status: str) -> "SpaceBuilder":
        """Define o status inicial do espaço"""
        opcoes_validas = {"DISPONIVEL", "RESERVADO", "MANUTENCAO"}
        if status not in opcoes_validas:
            raise ValueError(f"Status inválido. Use: {opcoes_validas}")
        self._status = status
        return self

    def com_timezone(self, timezone: str) -> "SpaceBuilder":
        """Define o fuso horário do espaço"""
        if not timezone or not timezone.strip():
            raise ValueError("Timezone não pode ser vazio")
        self._timezone = timezone
        return self

    def build(self) -> Space:
        """
        Constrói e retorna o objeto Space após validar campos obrigatórios.

        Raises:
            ValueError: Se esporte, localização ou preço não foram definidos.
        """
        if not self._esporte:
            raise ValueError("Esporte é obrigatório. Use .com_esporte()")
        if not self._localizacao:
            raise ValueError("Localização é obrigatória. Use .com_localizacao()")
        if self._preco_hora is None:
            raise ValueError("Preço por hora é obrigatório. Use .com_preco()")

        return Space(
            space_id=self._space_id,
            nome=self._nome,
            esporte=self._esporte,
            localizacao=self._localizacao,
            preco_hora=self._preco_hora,
            fotos=self._fotos,
            status=self._status,
            timezone=self._timezone,
        )
