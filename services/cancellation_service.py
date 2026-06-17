"""
CancellationService - Funcionalidade 9: Cancelamentos

Concito: Manipular cancelamentos de reservas com políticas
Propósito: Definir e gerenciar taxas de cancelamento
"""
from domain.booking import Booking
from services.base import BaseService
from typing import Dict
from datetime import datetime, timedelta


class CancellationService(BaseService):
    """Serviço para cancelamentos de reservas"""

    def __init__(self):
        super().__init__("CancellationService")
        self._politicas = self._inicializar_politicas()

    def _inicializar_politicas(self) -> Dict:
        """Inicializa políticas de cancelamento"""
        return {
            "mais_de_24h": {
                "descricao": "Cancelamento com 24h+ de antecedência",
                "taxa_percentual": 0,
                "taxa_fixa": 0,
                "reembolso_percentual": 100
            },
            "de_2_a_24h": {
                "descricao": "Cancelamento entre 2-24h de antecedência",
                "taxa_percentual": 50,
                "taxa_fixa": 0,
                "reembolso_percentual": 50
            },
            "menos_de_2h": {
                "descricao": "Cancelamento com menos de 2h",
                "taxa_percentual": 100,
                "taxa_fixa": 0,
                "reembolso_percentual": 0
            }
        }

    def obter_politicas_cancelamento(self) -> Dict:
        """Obtém todas as políticas de cancelamento"""
        return {
            "maisDe24h": self._politicas["mais_de_24h"]["descricao"],
            "de2a12h": self._politicas["de_2_a_24h"]["descricao"],
            "menosDe2h": self._politicas["menos_de_2h"]["descricao"]
        }

    def calcular_taxa_cancelamento(self, booking: Booking, tempo_antecedencia_horas: float) -> float:
        """
        Calcula taxa de cancelamento baseada no tempo

        Args:
            booking: Reserva a cancelar
            tempo_antecedencia_horas: Horas antes da hora da reserva

        Returns:
            Valor da taxa de cancelamento
        """
        self.validar_numero(tempo_antecedencia_horas, "Horas de antecedência", 0)

        if tempo_antecedencia_horas >= 24:
            politica = self._politicas["mais_de_24h"]
        elif tempo_antecedencia_horas >= 2:
            politica = self._politicas["de_2_a_24h"]
        else:
            politica = self._politicas["menos_de_2h"]

        taxa = booking.valor_total * (politica["taxa_percentual"] / 100)
        taxa += politica["taxa_fixa"]

        return taxa

    def calcular_reembolso(self, booking: Booking, tempo_antecedencia_horas: float) -> float:
        """Calcula o valor do reembolso"""
        taxa = self.calcular_taxa_cancelamento(booking, tempo_antecedencia_horas)
        reembolso = booking.valor_total - taxa

        return max(0, reembolso)

    def cancelar_com_politica(
        self,
        booking: Booking,
        tempo_antecedencia_horas: float
    ) -> Dict:
        """
        Cancela reserva com cálculo de política

        Args:
            booking: Reserva a cancelar
            tempo_antecedencia_horas: Horas antes da reserva

        Returns:
            Dicionário com detalhes do cancelamento
        """
        if booking.status in ["CANCELADO", "NAO_COMPARECEU"]:
            raise ValueError(f"Não é possível cancelar reserva {booking.status}")

        taxa = self.calcular_taxa_cancelamento(booking, tempo_antecedencia_horas)
        reembolso = self.calcular_reembolso(booking, tempo_antecedencia_horas)

        booking.cancelar(taxa)

        resultado = {
            "booking_id": booking.id,
            "valor_original": booking.valor_total,
            "taxa_cancelamento": taxa,
            "reembolso": reembolso,
            "tempo_antecedencia": tempo_antecedencia_horas,
            "status": booking.status
        }

        self.log(f"Reserva cancelada com política: {booking.id}")

        return resultado

    def obter_historico_cancelamentos(self) -> Dict:
        """Obtém histórico de cancelamentos"""
        return {
            "total_cancelamentos": 0,
            "taxa_media": 0,
            "reembolso_total": 0
        }

    def solicitar_reembolso(self, booking: Booking) -> bool:
        """Solicita reembolso para reserva cancelada"""
        if booking.status != "CANCELADO":
            raise ValueError("Apenas reservas canceladas podem ser reembolsadas")

        booking.reembolsar()
        self.log(f"Reembolso processado para a reserva {booking.id}")

        return True
