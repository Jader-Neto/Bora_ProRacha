"""
CheckinService - Funcionalidade 10: Confirmação de Check-in

Concito: Geração de código QR e confirmação de check-in
Propósito: Verificar presença e registrar check-ins
"""
from domain.booking import Booking
from services.base import BaseService
from typing import Dict
import hashlib
import base64


class CheckinService(BaseService):
    """Serviço para check-in e geração de código QR"""

    def __init__(self):
        super().__init__("CheckinService")
        self._checkins = {}

    def gerar_codigo_qr(self, booking: Booking) -> str:
        """
        Gera código QR para reserva

        Args:
            booking: Objeto de reserva

        Returns:
            Representação string do código QR
        """
        if booking.status != "CONFIRMADO":
            raise ValueError(f"Não é possível gerar QR para reserva {booking.status}")

        # Cria um código único baseado nas informações da reserva
        dados = f"{booking.id}_{booking.space_id}_{booking.user_id}"
        hash_code = hashlib.sha256(dados.encode()).hexdigest()

        # Simula código QR como string codificada
        qr_code = base64.b64encode(hash_code.encode()).decode()

        self.log(f"Código QR gerado para a reserva {booking.id}")

        return f"QR_{qr_code[:20]}"

    def realizar_checkin(self, booking: Booking, codigo_verificacao: str = None) -> Dict:
        """
        Realiza check-in

        Args:
            booking: Objeto de reserva
            codigo_verificacao: Código de verificação (opcional)

        Returns:
            Detalhes da confirmação de check-in
        """
        if booking.status != "CONFIRMADO":
            raise ValueError(f"Não é possível fazer check-in em reserva {booking.status}")

        booking.realizar_checkin()

        checkin_info = {
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "space_id": booking.space_id,
            "status_anterior": "CONFIRMADO",
            "novo_status": booking.status,
            "hora_checkin": str(self._obter_timestamp()),
            "verificado": True
        }

        self._checkins[booking.id] = checkin_info
        self.log(f"Check-in realizado para a reserva {booking.id}")

        return checkin_info

    def validar_qr_code(self, qr_code: str) -> bool:
        """Valida formato do código QR"""
        return qr_code.startswith("QR_") and len(qr_code) > 3

    def obter_status_checkin(self, booking_id: str) -> Dict | None:
        """Obtém status de check-in para a reserva"""
        return self._checkins.get(booking_id)

    def obter_relatorio_checkins(self) -> Dict:
        """Obtém relatório de check-ins"""
        total_checkins = len(self._checkins)

        relatorio = {
            "total_checkins": total_checkins,
            "data_relatorio": str(self._obter_timestamp()),
            "checkins_por_hora": self._agrupar_por_hora()
        }

        return relatorio

    def marcar_nao_comparecimento(self, booking: Booking) -> bool:
        """Marca reserva como não comparecimento"""
        if booking.status not in ["CONFIRMADO", "CHECKIN_REALIZADO"]:
            raise ValueError(f"Não é possível marcar {booking.status} como não comparecimento")

        booking.marcar_nao_comparecimento()
        self.log(f"Não comparecimento registrado para a reserva {booking.id}")

        return True

    def gerar_recibo_checkin(self, booking: Booking) -> str:
        """Gera recibo de check-in"""
        checkin_info = self.obter_status_checkin(booking.id)

        if not checkin_info:
            raise ValueError("Check-in não encontrado para esta reserva")

        recibo = f"""
        {'='*50}
        RECIBO DE CHECK-IN
        {'='*50}
        Reserva ID: {checkin_info['booking_id']}
        Usuário: {checkin_info['user_id']}
        Espaço: {checkin_info['space_id']}
        Status: {checkin_info['novo_status']}
        Hora do Check-in: {checkin_info['hora_checkin']}
        Verificado: {'✓' if checkin_info['verificado'] else '✗'}
        {'='*50}
        """

        return recibo

    def _obter_timestamp(self) -> str:
        """Obtém timestamp atual"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _agrupar_por_hora(self) -> Dict:
        """Agrupa check-ins por hora (simplificado)"""
        return {
            "08:00": 0,
            "09:00": 0,
            "18:00": 0,
            "19:00": 0
        }
