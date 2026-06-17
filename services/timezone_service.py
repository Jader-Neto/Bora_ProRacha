"""
TimezoneService - Funcionalidade 8: Fuso Horário Dinâmico

Concito: Manipular diferentes fusos horários para espaços
Propósito: Suportar sistema de reservas multi-região
"""
from domain.space import Space
from services.base import BaseService
from typing import Dict, List


class TimezoneService(BaseService):
    """Serviço para gerenciamento de fusos horários"""

    def __init__(self):
        super().__init__("TimezoneService")
        self._timezones_validos = [
            "America/Sao_Paulo",
            "America/Manaus",
            "America/Anchorage",
            "America/New_York",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney",
            "UTC"
        ]

    def ajustar_timezone(self, space: Space, novo_timezone: str = "America/Sao_Paulo") -> Space:
        """
        Ajusta fuso horário do espaço

        Args:
            space: Objeto do espaço
            novo_timezone: Novo fuso horário (padrão: São Paulo)

        Returns:
            Espaço atualizado
        """
        if novo_timezone not in self._timezones_validos:
            self.aviso(f"Fuso horário {novo_timezone} não está na lista padrão, definindo mesmo assim")

        space.timezone = novo_timezone
        self.log(f"Fuso horário do espaço {space.nome} ajustado para {novo_timezone}")

        return space

    def validar_timezone(self, timezone: str) -> bool:
        """Valida se o fuso horário é válido"""
        return timezone in self._timezones_validos

    def obter_timezones_disponiveis(self) -> List[str]:
        """Obtém lista de fusos horários disponíveis"""
        return self._timezones_validos.copy()

    def converter_horario(
        self,
        horario_str: str,
        de_timezone: str,
        para_timezone: str
    ) -> str:
        """
        Converte hora entre fusos horários

        Args:
            horario_str: String da hora
            de_timezone: Fuso horário de origem
            para_timezone: Fuso horário de destino

        Returns:
            String da hora convertida (simplificado - para demonstração)
        """
        if not self.validar_timezone(de_timezone):
            raise ValueError(f"Fuso horário inválido: {de_timezone}")
        if not self.validar_timezone(para_timezone):
            raise ValueError(f"Fuso horário inválido: {para_timezone}")

        # Simplificado - em aplicação real usaria biblioteca pytz
        diferenca = self._calcular_diferenca_horas(de_timezone, para_timezone)
        self.log(f"Hora convertida de {de_timezone} para {para_timezone} (dif: {diferenca}h)")

        return f"{horario_str} ({para_timezone})"

    def _calcular_diferenca_horas(self, tz1: str, tz2: str) -> int:
        """Calcula diferença de horas entre fusos horários (simplificado)"""
        # Diferenças de fuso horário simplificadas relativas a UTC
        offsets = {
            "UTC": 0,
            "America/Sao_Paulo": -3,
            "America/New_York": -5,
            "Europe/London": 0,
            "Europe/Paris": 1,
            "Asia/Tokyo": 9,
            "Asia/Shanghai": 8,
            "Australia/Sydney": 10,
        }

        offset1 = offsets.get(tz1, 0)
        offset2 = offsets.get(tz2, 0)

        return offset2 - offset1

    def obter_relatorio_timezones(self, spaces: List[Space]) -> Dict:
        """Obtém relatório de distribuição de fusos horários"""
        if not spaces:
            return {}

        tz_count = {}
        for space in spaces:
            tz = space.timezone
            tz_count[tz] = tz_count.get(tz, 0) + 1

        relatorio = {
            "total_espacos": len(spaces),
            "distribuicao_timezones": tz_count,
            "timezones_unicos": len(tz_count)
        }

        return relatorio
