"""
Suite de testes para serviços
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.space import Space
from domain.user import User
from domain.booking import Booking
from domain.timeslot import TimeSlot
from datetime import datetime, timedelta

from services.filter_service import FilterService
from services.quick_registration_service import QuickRegistrationService
from services.easy_booking_service import EasyBookingService
from services.detailed_space_service import DetailedSpaceService
from services.reminder_service import ReminderService
from services.timezone_service import TimezoneService
from services.cancellation_service import CancellationService
from services.checkin_service import CheckinService


class TestFilterService:
    """Testar FilterService"""

    @pytest.fixture
    def spaces(self):
        return [
            Space("s1", "Arena 1", "Futebol", "Maceió", 100, ["f1.jpg"]),
            Space("s2", "Arena 2", "Vôlei", "Maceió", 150, ["f2.jpg"]),
            Space("s3", "Arena 3", "Basquete", "São Paulo", 200, ["f3.jpg"]),
        ]

    def test_filtrar_por_local(self, spaces):
        service = FilterService()
        resultado = service.filtrar_por_local(spaces, "Maceió")
        assert len(resultado) == 2

    def test_filtrar_por_esporte(self, spaces):
        service = FilterService()
        resultado = service.filtrar_por_esporte(spaces, "Futebol")
        assert len(resultado) == 1
        assert resultado[0].esporte == "Futebol"

    def test_filtrar_por_preco(self, spaces):
        service = FilterService()
        resultado = service.filtrar_por_preco(spaces, 150)
        assert len(resultado) == 2

    def test_ordenar_por_preco(self, spaces):
        service = FilterService()
        resultado = service.ordenar_por_preco(spaces)
        assert resultado[0].preco_hora == 100
        assert resultado[-1].preco_hora == 200

    def test_filtrar_avancado(self, spaces):
        service = FilterService()
        resultado = service.filtrar_avancado(
            spaces,
            local="Maceió",
            preco_maximo=150
        )
        assert len(resultado) == 2


class TestQuickRegistrationService:
    """Test QuickRegistrationService"""

    def test_login_com_google(self):
        service = QuickRegistrationService()
        usuario = service.login_com_google("test@gmail.com")
        assert usuario.email == "test@gmail.com"
        assert usuario.status == "CADASTRO_PARCIAL"

    def test_obter_progresso_cadastro(self):
        service = QuickRegistrationService()
        usuario = service.login_com_google("test@gmail.com")
        progresso = service.obter_progresso_cadastro(usuario)
        assert progresso == 50

    def test_completar_cadastro(self):
        service = QuickRegistrationService()
        usuario = service.login_com_google("test@gmail.com")
        usuario_completo = service.completar_cadastro(usuario, "85987654321")
        assert usuario_completo.status == "CADASTRO_COMPLETO"


class TestEasyBookingService:
    """Test EasyBookingService"""

    def test_selecionar_horario(self):
        service = EasyBookingService()
        inicio = datetime.now()
        fim = inicio + timedelta(hours=1)
        slot = TimeSlot("t1", "s1", inicio, fim)
        resultado = service.selecionar_horario(slot)
        assert resultado.id == "t1"

    def test_criar_reserva_rapida(self):
        service = EasyBookingService()
        reserva = service.criar_reserva_rapida("u1", "s1", "t1", 100.0)
        assert reserva.user_id == "u1"
        assert reserva.status == "RESERVADO"

    def test_confirmar_reserva(self):
        service = EasyBookingService()
        reserva = service.criar_reserva_rapida("u1", "s1", "t1", 100.0)
        reserva_confirmada = service.confirmar_reserva(reserva)
        assert reserva_confirmada.status == "CONFIRMADO"


class TestDetailedSpaceService:
    """Test DetailedSpaceService"""

    def test_obter_detalhes_espaco(self):
        service = DetailedSpaceService()
        space = Space("s1", "Arena 1", "Futebol", "Maceió", 100, ["f1.jpg"])
        detalhes = service.obter_detalhes_espaco(space)
        assert detalhes["nome"] == "Arena 1"
        assert detalhes["preco_hora"] == 100

    def test_adicionar_avaliacao(self):
        service = DetailedSpaceService()
        media = service.adicionar_avaliacao("s1", 5)
        service.adicionar_avaliacao("s1", 4)
        media_final = service.obter_media_avaliacoes("s1")
        assert media_final == 4.5

    def test_adicionar_comentario(self):
        service = DetailedSpaceService()
        service.adicionar_comentario("s1", "Muito bom!")
        comentarios = service.obter_comentarios("s1")
        assert len(comentarios) == 1
        assert "Muito bom!" in comentarios


class TestReminderService:
    """Test ReminderService"""

    def test_agendar_lembrete(self):
        service = ReminderService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        lembrete = service.agendar_lembrete(booking)
        assert lembrete.user_id == "u1"
        assert lembrete.status == "PENDENTE"

    def test_enviar_todos_lembretes(self):
        service = ReminderService()
        booking1 = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        booking2 = Booking("bk2", "u2", "s2", "t2", "CONFIRMADO", 150.0)
        service.agendar_lembrete(booking1)
        service.agendar_lembrete(booking2)
        enviados = service.enviar_todos_lembretes()
        assert enviados == 2


class TestTimezoneService:
    """Test TimezoneService"""

    def test_validar_timezone(self):
        service = TimezoneService()
        assert service.validar_timezone("America/Sao_Paulo") is True
        assert service.validar_timezone("Invalid/Timezone") is False

    def test_obter_timezones_disponiveis(self):
        service = TimezoneService()
        timezones = service.obter_timezones_disponiveis()
        assert "America/Sao_Paulo" in timezones
        assert len(timezones) > 0

    def test_converter_horario(self):
        service = TimezoneService()
        resultado = service.converter_horario(
            "18:00",
            "America/Sao_Paulo",
            "UTC"
        )
        assert "18:00" in resultado


class TestCancellationService:
    """Test CancellationService"""

    def test_calcular_taxa_mais_24h(self):
        service = CancellationService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        taxa = service.calcular_taxa_cancelamento(booking, 25)
        assert taxa == 0  # No fee with 24h+ notice

    def test_calcular_taxa_2_24h(self):
        service = CancellationService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        taxa = service.calcular_taxa_cancelamento(booking, 12)
        assert taxa == 50.0  # 50% fee

    def test_cancelar_com_politica(self):
        service = CancellationService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        resultado = service.cancelar_com_politica(booking, 25)
        assert resultado["reembolso"] == 100.0
        assert booking.status == "CANCELADO"


class TestCheckinService:
    """Test CheckinService"""

    def test_gerar_codigo_qr(self):
        service = CheckinService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        qr = service.gerar_codigo_qr(booking)
        assert qr.startswith("QR_")

    def test_realizar_checkin(self):
        service = CheckinService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        checkin_info = service.realizar_checkin(booking)
        assert checkin_info["novo_status"] == "CHECKIN_REALIZADO"
        assert booking.status == "CHECKIN_REALIZADO"

    def test_marcar_nao_comparecimento(self):
        service = CheckinService()
        booking = Booking("bk1", "u1", "s1", "t1", "CONFIRMADO", 100.0)
        resultado = service.marcar_nao_comparecimento(booking)
        assert resultado is True
        assert booking.status == "NAO_COMPARECEU"
