"""
DynamicSpaceRegistrationService - Funcionalidade 6: Registro Dinâmico de Espaços

Concito: Permitir proprietários de espaços registrar seus espaços
Propósito: Expandir espaços disponíveis dinamicamente
"""
from typing import Dict
from domain.space import Space
from domain.space_builder import SpaceBuilder
from services.base import BaseService
import uuid


class DynamicSpaceRegistrationService(BaseService):
    """Serviço para registro dinâmico de espaços"""

    def __init__(self):
        super().__init__("DynamicSpaceRegistrationService")
        self._espacos_registrados = {}

    def cadastrar_espaco(
        self,
        nome: str,
        esporte: str,
        localizacao: str,
        preco_hora: float,
        timezone: str,
        fotos: list
    ) -> Space:
        """
        Registra novo espaço de esportes usando SpaceBuilder.

        Args:
            nome: Nome do espaço
            esporte: Tipo de esporte
            localizacao: Localização
            preco_hora: Preço por hora
            timezone: Fuso horário
            fotos: Lista de URLs de fotos

        Returns:
            Espaço criado
        """
        self.validar_string(nome, "Nome do espaço")
        self.validar_string(esporte, "Esporte")
        self.validar_string(localizacao, "Localização")
        self.validar_numero(preco_hora, "Preço por hora", 1)
        self.validar_string(timezone, "Fuso horário")
        self.validar_lista(fotos, "Fotos")

        space_id = f"sp_{uuid.uuid4().hex[:8]}"

        space = (SpaceBuilder(space_id, nome)
            .com_esporte(esporte)
            .com_localizacao(localizacao)
            .com_preco(preco_hora)
            .com_fotos(fotos)
            .com_timezone(timezone)
            .com_status("DISPONIVEL")
            .build())

        self._espacos_registrados[space_id] = space
        self.log(f"Espaço registrado: {nome} (ID: {space_id})")
        return space

    def atualizar_espaco(self, space: Space) -> Space:
        """Atualiza informações do espaço"""
        if space.id not in self._espacos_registrados:
            raise ValueError(f"Espaço {space.id} não encontrado")

        self._espacos_registrados[space.id] = space
        self.log(f"Espaço atualizado: {space.nome}")
        return space

    def remover_espaco(self, space_id: str) -> bool:
        """Remove espaço do registro"""
        if space_id not in self._espacos_registrados:
            return False

        del self._espacos_registrados[space_id]
        self.log(f"Espaço removido: {space_id}")
        return True

    def obter_espacos_registrados(self) -> list:
        """Obtém todos os espaços registrados"""
        return list(self._espacos_registrados.values())

    def verificar_disponibilidade(self, space_id: str) -> bool:
        """Verifica se o espaço está disponível"""
        if space_id not in self._espacos_registrados:
            return False

        space = self._espacos_registrados[space_id]
        return space.status == "DISPONIVEL"

    def obter_relatorio_registro(self) -> Dict:
        """Obtém relatório de registro"""
        espacos = self.obter_espacos_registrados()

        relatorio = {
            "total_espacos": len(espacos),
            "espacos_disponiveis": len([e for e in espacos if e.status == "DISPONIVEL"]),
            "espacos_em_manutencao": len([e for e in espacos if e.status == "MANUTENCAO"]),
            "esportes": list(set(e.esporte for e in espacos)),
            "locais": list(set(e.localizacao for e in espacos)),
            "preco_medio": sum(e.preco_hora for e in espacos) / len(espacos) if espacos else 0
        }

        return relatorio

