"""
BookingFacade — Padrão Facade

Problema resolvido: o app.py orquestrava manualmente múltiplos serviços
dentro de cada rota (criar slot → criar reserva → confirmar → agendar
lembrete → gerar QR → fazer checkin → cancelar com política). Isso
vazava lógica de negócio para a camada HTTP e obrigava qualquer novo
cliente (CLI, testes, outro endpoint) a replicar toda a orquestração.

Solução: BookingFacade centraliza os fluxos completos de negócio.
As rotas do app.py passam a chamar um único método por operação,
sem conhecer os serviços internos.

Fluxos encapsulados:
  - reservar()         → criar slot + booking + confirmar + lembrete
  - fazer_checkin()    → gerar QR + realizar checkin
  - cancelar()         → cancelar com política + reembolso opcional
  - agendar_lembrete() → delegar ao ReminderService
"""
from datetime import datetime, timedelta
from typing import Dict
import time

from domain.booking import Booking
from domain.timeslot import TimeSlot
from domain.notification import Notification
from services.easy_booking_service import EasyBookingService
from services.checkin_service import CheckinService
from services.cancellation_service import CancellationService
from services.reminder_service import ReminderService


def _gen_id(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


class BookingFacade:
    """
    Fachada para operações de reserva.
    Orquestra EasyBookingService, CheckinService,
    CancellationService e ReminderService.
    """

    def __init__(
        self,
        booking_service: EasyBookingService | None = None,
        checkin_service: CheckinService | None = None,
        cancellation_service: CancellationService | None = None,
        reminder_service: ReminderService | None = None,
    ):
        self._booking_svc = booking_service or EasyBookingService()
        self._checkin_svc = checkin_service or CheckinService()
        self._cancellation_svc = cancellation_service or CancellationService()
        self._reminder_svc = reminder_service or ReminderService()

    # ── Fluxo completo de reserva ──────────────────────────────────────────
    def reservar(
        self,
        user_id: str,
        space_id: str,
        valor: float,
        local: str = "",
        horario: str = "",
        horas_lembrete: int = 24,
        metodo_pagamento: str = "Cartão de Crédito",
        ultimos4: str = "0000",
    ) -> Dict:
        """
        Cria slot, reserva, confirma e agenda lembrete em uma única chamada.

        Returns:
            Dict com reserva e pagamento prontos para serialização JSON.
        """
        agora = datetime.now()
        inicio = agora + timedelta(hours=1)
        fim = inicio + timedelta(hours=2)

        slot = TimeSlot(
            slot_id=_gen_id("ts"),
            space_id=space_id,
            inicio=inicio,
            fim=fim,
            status="DISPONIVEL",
        )

        booking = self._booking_svc.criar_reserva_rapida(
            user_id=user_id,
            space_id=space_id,
            slot_id=slot.id,
            valor_total=float(valor) if valor else 0.0,
        )
        booking.confirmar()

        self._reminder_svc.agendar_lembrete(booking, horas_lembrete)

        pagamento = {
            "id": _gen_id("p"),
            "reservaId": booking.id,
            "metodo": metodo_pagamento,
            "ultimos4": ultimos4,
            "valor": valor,
            "data": agora.strftime("%d/%m/%Y"),
            "status": "Aprovado",
        }

        return {
            "reserva": {
                "id": booking.id,
                "user_id": booking.user_id,
                "space_id": booking.space_id,
                "local": local,
                "horario": horario,
                "status": booking.status,
                "data": agora.strftime("%d/%m/%Y"),
                "valor": str(valor),
            },
            "pagamento": pagamento,
        }

    # ── Fluxo de check-in ──────────────────────────────────────────────────
    def fazer_checkin(self, booking_id: str, user_id: str = "demo_user") -> Dict:
        """
        Gera QR Code e realiza check-in em uma única chamada.

        Returns:
            Dict com reserva_id, qr_code, detalhes do checkin e status.
        """
        booking = Booking(
            booking_id=booking_id,
            user_id=user_id,
            space_id="demo_space",
            slot_id="demo_slot",
            status="CONFIRMADO",
        )

        qr_code = self._checkin_svc.gerar_codigo_qr(booking)
        checkin_info = self._checkin_svc.realizar_checkin(booking)

        return {
            "reserva_id": booking_id,
            "qr_code": qr_code,
            "checkin": checkin_info,
            "status": booking.status,
        }

    # ── Fluxo de cancelamento ──────────────────────────────────────────────
    def cancelar(
        self,
        booking_id: str,
        tempo_antecedencia_horas: float = 24,
        valor_total: float = 100.0,
        solicitar_reembolso: bool = False,
    ) -> Dict:
        """
        Cancela reserva com política e opcionalmente processa reembolso.

        Returns:
            Dict com detalhes do cancelamento (e reembolso se solicitado).
        """
        booking = Booking(
            booking_id=booking_id,
            user_id="demo_user",
            space_id="demo_space",
            slot_id="demo_slot",
            status="CONFIRMADO",
            valor_total=valor_total,
        )

        resultado = self._cancellation_svc.cancelar_com_politica(
            booking, tempo_antecedencia_horas
        )

        if solicitar_reembolso and booking.status == "CANCELADO":
            self._cancellation_svc.solicitar_reembolso(booking)
            resultado["reembolso_solicitado"] = True
            resultado["status_final"] = booking.status

        return resultado

    # ── Agendamento de lembrete avulso ─────────────────────────────────────
    def agendar_lembrete(
        self,
        booking_id: str,
        user_id: str = "demo_user",
        horas_antes: int = 24,
    ) -> Dict:
        """
        Agenda lembrete para uma reserva existente.

        Returns:
            Dict com dados da notificação criada.
        """
        booking = Booking(
            booking_id=booking_id,
            user_id=user_id,
            space_id="demo_space",
            slot_id="demo_slot",
            status="CONFIRMADO",
        )

        notificacao: Notification = self._reminder_svc.agendar_lembrete(
            booking, horas_antes
        )

        return {
            "id": notificacao.id,
            "user_id": notificacao.user_id,
            "titulo": notificacao.titulo,
            "mensagem": notificacao.mensagem,
            "status": notificacao.status,
        }
