"""
Espaço - Entidade representando um espaço de esporte disponível para reserva
Com encapsulamento: atributos protegidos e validação em modificadores
"""
from typing import Literal, List

from .base import BaseEntity

SpaceStatus = Literal["DISPONIVEL", "RESERVADO", "MANUTENCAO"]


class Space(BaseEntity):
    """
    Entidade de espaço de esporte com encapsulamento e validação.
    """
    def __init__(
        self,
        space_id: str,
        nome: str,
        esporte: str,
        localizacao: str,
        preco_hora: float,
        fotos: List[str],
        status: SpaceStatus = "DISPONIVEL",
        timezone: str = "America/Sao_Paulo"
    ):
        super().__init__(space_id)
        self._nome = nome
        self._esporte = esporte
        self._localizacao = localizacao
        self._preco_hora = preco_hora
        self._fotos = fotos.copy()
        self._status = status
        self._timezone = timezone
        self._avaliacoes: List[int] = []
        self._validar()

    def _validar(self) -> None:
        """Validar dados do espaço"""
        if self._preco_hora <= 0:
            raise ValueError("Preço por hora deve ser maior que zero")
        if not self._timezone or not self._timezone.strip():
            raise ValueError("Timezone é obrigatório")

    # Propriedades
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def esporte(self) -> str:
        return self._esporte

    @property
    def localizacao(self) -> str:
        return self._localizacao

    @property
    def preco_hora(self) -> float:
        return self._preco_hora

    @property
    def fotos(self) -> List[str]:
        return self._fotos.copy()

    @property
    def status(self) -> SpaceStatus:
        return self._status

    @property
    def timezone(self) -> str:
        return self._timezone

    @property
    def avaliacoes(self) -> List[int]:
        return self._avaliacoes.copy()

    # Modificadores com validação
    @status.setter
    def status(self, novo_status: SpaceStatus) -> None:
        self._status = novo_status

    @timezone.setter
    def timezone(self, novo_timezone: str) -> None:
        if not novo_timezone or not novo_timezone.strip():
            raise ValueError("Timezone não pode ser vazio")
        self._timezone = novo_timezone

    # Métodos de negócio
    def entrar_em_manutencao(self) -> None:
        """Colocar espaço em manutenção"""
        self._status = "MANUTENCAO"

    def atualizar_preco(self, novo_preco: float) -> None:
        """Atualizar preço"""
        if novo_preco <= 0:
            raise ValueError("Novo preço deve ser maior que zero")
        self._preco_hora = novo_preco

    def adicionar_avaliacao(self, nota: int) -> None:
        """Add rating (1-5)"""
        if not 1 <= nota <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self._avaliacoes.append(nota)

    def obter_media_avaliacoes(self) -> float:
        """Get average rating"""
        if not self._avaliacoes:
            return 0.0
        return sum(self._avaliacoes) / len(self._avaliacoes)

    def adicionar_foto(self, url: str) -> None:
        """Add photo"""
        if url and url.strip():
            self._fotos.append(url)

    def __repr__(self):
        return (f"Space(id={self.id}, nome={self._nome}, esporte={self._esporte}, "
                f"localizacao={self._localizacao}, status={self._status})")
