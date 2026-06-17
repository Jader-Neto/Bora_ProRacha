"""
DetailedSpaceService - Funcionalidade 5: Espaços Detalhados

Concito: Informação abrangente do espaço e avaliações
Propósito: Fornecer informações detalhadas e feedback de clientes
"""
from typing import Dict, List

from domain.space import Space
from services.base import BaseService


class DetailedSpaceService(BaseService):
    """Serviço para informações detalhadas do espaço"""

    def __init__(self):
        super().__init__("DetailedSpaceService")
        self._avaliacoes: Dict[str, List[int]] = {}
        self._comentarios: Dict[str, List[str]] = {}

    def obter_detalhes_espaco(self, space: Space) -> Dict:
        """
        Obtém detalhes abrangentes do espaço

        Args:
            space: Objeto do espaço

        Returns:
            Dicionário com detalhes do espaço
        """
        media_avaliacoes = space.obter_media_avaliacoes()
        total_avaliacoes = len(space.avaliacoes)
        comentarios = self._comentarios.get(space.id, [])

        detalhes = {
            "id": space.id,
            "nome": space.nome,
            "esporte": space.esporte,
            "localizacao": space.localizacao,
            "preco_hora": space.preco_hora,
            "fotos": space.fotos,
            "status": space.status,
            "timezone": space.timezone,
            "avaliacao_media": round(media_avaliacoes, 2),
            "total_avaliacoes": total_avaliacoes,
            "comentarios": comentarios,
            "total_comentarios": len(comentarios)
        }

        self.log(f"Detalhes do espaço obtidos: {space.nome}")
        return detalhes

    def adicionar_avaliacao(self, space_id: str, nota: int) -> float:
        """
        Adiciona avaliação ao espaço

        Args:
            space_id: ID do espaço
            nota: Avaliação (1-5)

        Returns:
            Avaliação média após adicionar
        """
        if not 1 <= nota <= 5:
            raise ValueError("A avaliação deve estar entre 1 e 5")

        if space_id not in self._avaliacoes:
            self._avaliacoes[space_id] = []

        self._avaliacoes[space_id].append(nota)
        media = self.obter_media_avaliacoes(space_id)

        self.log(f"Avaliação adicionada ao espaço {space_id}: {nota} ⭐")
        return media

    def obter_media_avaliacoes(self, space_id: str) -> float:
        """Obtém avaliação média para o espaço"""
        avaliacoes = self._avaliacoes.get(space_id, [])
        if not avaliacoes:
            return 0.0
        return sum(avaliacoes) / len(avaliacoes)

    def adicionar_comentario(self, space_id: str, comentario: str) -> None:
        """Adiciona comentário ao espaço"""
        self.validar_string(comentario, "Comentário")

        if space_id not in self._comentarios:
            self._comentarios[space_id] = []

        self._comentarios[space_id].append(comentario)
        self.log(f"Comentário adicionado ao espaço {space_id}")

    def obter_comentarios(self, space_id: str) -> List[str]:
        """Obtém todos os comentários para o espaço"""
        return self._comentarios.get(space_id, [])

    def gerar_relatorio_espaco(self, space: Space) -> str:
        """Gera relatório abrangente do espaço"""
        detalhes = self.obter_detalhes_espaco(space)

        relatorio = f"""
        {'='*50}
        RELATÓRIO DO ESPAÇO
        {'='*50}
        Nome: {detalhes['nome']}
        Esporte: {detalhes['esporte']}
        Local: {detalhes['localizacao']}
        Preço: R$ {detalhes['preco_hora']}/h
        Status: {detalhes['status']}
        Avaliação: {'⭐' * int(detalhes['avaliacao_media'])} ({detalhes['avaliacao_media']}/5)
        Total de Avaliações: {detalhes['total_avaliacoes']}
        Comentários: {detalhes['total_comentarios']}
        {'='*50}
        """

        return relatorio
