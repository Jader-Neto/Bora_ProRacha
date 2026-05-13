"""
Suite de testes para entidades de domínio
"""
import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.user import User
from domain.space import Space
from domain.booking import Booking
from domain.timeslot import TimeSlot
from domain.notification import Notification


class TestUser:
    """Testar entidade de Usuário"""

    def test_create_user(self):
        user = User("u1", "John", "john@email.com", None, "NAO_CADASTRADO")
        assert user.id == "u1"
        assert user.nome == "John"
        assert user.email == "john@email.com"
        assert user.status == "NAO_CADASTRADO"

    def test_invalid_email(self):
        with pytest.raises(ValueError):
            User("u1", "John", "invalid-email", None, "NAO_CADASTRADO")

    def test_complete_registration(self):
        user = User("u1", "John", "john@email.com", None, "CADASTRO_PARCIAL")
        user.completar_cadastro("85987654321")
        assert user.status == "CADASTRO_COMPLETO"
        assert user.telefone == "85987654321"

    def test_pode_reservar(self):
        user1 = User("u1", "John", "john@email.com", "85987654321", "CADASTRO_COMPLETO")
        assert user1.pode_reservar() is True

        user2 = User("u2", "Jane", "jane@email.com", None, "CADASTRO_PARCIAL")
        assert user2.pode_reservar() is False


class TestSpace:
    """Testar entidade de Espaço"""

    def test_create_space(self):
        space = Space(
            "s1",
            "Quadra 1",
            "Futebol",
            "Maceió",
            100,
            ["foto1.jpg"],
            "DISPONIVEL"
        )
        assert space.id == "s1"
        assert space.nome == "Quadra 1"
        assert space.status == "DISPONIVEL"

    def test_invalid_price(self):
        with pytest.raises(ValueError):
            Space(
                "s1",
                "Quadra 1",
                "Futebol",
                "Maceió",
                -100,  # Preço negativo inválido
                ["foto1.jpg"]
            )

    def test_update_price(self):
        space = Space("s1", "Quadra 1", "Futebol", "Maceió", 100, ["foto1.jpg"])
        space.atualizar_preco(150)
        assert space.preco_hora == 150

    def test_adicionar_avaliacao(self):
        space = Space("s1", "Quadra 1", "Futebol", "Maceió", 100, ["foto1.jpg"])
        space.adicionar_avaliacao(5)
        space.adicionar_avaliacao(4)
        media = space.obter_media_avaliacoes()
        assert media == 4.5

    def test_manutencao(self):
        space = Space("s1", "Quadra 1", "Futebol", "Maceió", 100, ["foto1.jpg"])
        space.entrar_em_manutencao()
        assert space.status == "MANUTENCAO"


class TestTimeSlot:
    """Testar entidade de Intervalo de Tempo"""

    def test_create_slot(self):
        inicio = datetime.now()
        fim = inicio + timedelta(hours=1)
        slot = TimeSlot("t1", "s1", inicio, fim)
        assert slot.id == "t1"
        assert slot.space_id == "s1"
        assert slot.status == "DISPONIVEL"

    def test_duracao_horas(self):
        inicio = datetime.now()
        fim = inicio + timedelta(hours=2)
        slot = TimeSlot("t1", "s1", inicio, fim)
        assert slot.duracao_horas() == 2.0

    def test_reservar_slot(self):
        inicio = datetime.now()
        fim = inicio + timedelta(hours=1)
        slot = TimeSlot("t1", "s1", inicio, fim)
        slot.reservar()
        assert slot.status == "RESERVADO"

    def test_libertar_slot(self):
        inicio = datetime.now()
        fim = inicio + timedelta(hours=1)
        slot = TimeSlot("t1", "s1", inicio, fim, "RESERVADO")
        slot.liberar()
        assert slot.status == "DISPONIVEL"

    def test_bloquear_slot(self):
        inicio = datetime.now()
        fim = inicio + timedelta(hours=1)
        slot = TimeSlot("t1", "s1", inicio, fim)
        slot.bloquear()
        assert slot.status == "BLOQUEADO"


class TestBooking:
    """Testar entidade de Reserva"""

    def test_create_booking(self):
        booking = Booking(
            "bk1",
            "u1",
            "s1",
            "t1",
            "RESERVADO",
            100.0
        )
        assert booking.id == "bk1"
        assert booking.user_id == "u1"
        assert booking.status == "RESERVADO"

    def test_confirmar_booking(self):
        booking = Booking(
            "bk1",
            "u1",
            "s1",
            "t1",
            "RESERVADO",
            100.0
        )
        booking.confirmar()
        assert booking.status == "CONFIRMADO"

    def test_cancelar_booking(self):
        booking = Booking(
            "bk1",
            "u1",
            "s1",
            "t1",
            "CONFIRMADO",
            100.0
        )
        booking.cancelar(20.0)
        assert booking.status == "CANCELADO"
        assert booking.taxa_cancelamento == 20.0

    def test_reembolso_calculo(self):
        booking = Booking(
            "bk1",
            "u1",
            "s1",
            "t1",
            "CANCELADO",
            100.0,
            25.0
        )
        assert booking.reembolso == 75.0

    def test_checkin(self):
        booking = Booking(
            "bk1",
            "u1",
            "s1",
            "t1",
            "CONFIRMADO",
            100.0
        )
        booking.realizar_checkin()
        assert booking.status == "CHECKIN_REALIZADO"


class TestNotification:
    """Testar entidade de Notificação"""

    def test_create_notification(self):
        notif = Notification(
            "n1",
            "u1",
            "Test",
            "Test message",
            "EMAIL"
        )
        assert notif.id == "n1"
        assert notif.status == "PENDENTE"

    def test_marcar_enviada(self):
        notif = Notification(
            "n1",
            "u1",
            "Test",
            "Test message"
        )
        notif.marcar_enviada()
        assert notif.status == "ENVIADA"
        assert notif.data_envio is not None

    def test_marcar_lida(self):
        notif = Notification(
            "n1",
            "u1",
            "Test",
            "Test message",
            "EMAIL",
            "ENVIADA"
        )
        notif.marcar_lida()
        assert notif.status == "LIDA"

    def test_marcar_falha(self):
        notif = Notification(
            "n1",
            "u1",
            "Test",
            "Test message",
            "EMAIL",
            "PENDENTE"
        )
        notif.marcar_falha()
        assert notif.status == "FALHA"
