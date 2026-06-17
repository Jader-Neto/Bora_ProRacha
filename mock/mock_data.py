"""
Dados Simulados - Dados de exemplo para desenvolvimento e testes
"""
from datetime import datetime, timedelta

from domain.user import User
from domain.space import Space
from domain.space_builder import SpaceBuilder
from domain.timeslot import TimeSlot
from domain.booking import Booking
from domain.notification import Notification


# ============ USUÁRIOS SIMULADOS ============
mock_users = [
    User("u1", "Pedro", "pedro@email.com", None, "CADASTRO_PARCIAL"),
    User("u2", "Maria Silva", "maria@email.com", "85987654321", "CADASTRO_COMPLETO"),
    User("u3", "João Santos", "joao@email.com", "85988888888", "CADASTRO_COMPLETO"),
    User("u4", "Ana Costa", "ana@email.com", None, "NAO_CADASTRADO")
]

# ============ ESPAÇOS SIMULADOS ============
mock_spaces = [
    # Espaços em Maceió
    SpaceBuilder("s1", "Arena Pajuçara")
        .com_esporte("Futebol")
        .com_localizacao("Pajuçara, Maceió - AL, Av. Dr. Antônio Gouveia, 150")
        .com_preco(120)
        .com_fotos(["https://example.com/foto1.jpg", "https://example.com/foto2.jpg"])
        .com_status("DISPONIVEL")
        .com_timezone("America/Sao_Paulo")
        .build(),

    SpaceBuilder("s2", "Quadra Jatiúca")
        .com_esporte("Vôlei")
        .com_localizacao("Jatiúca, Maceió - AL, Rua Carlos Jundiaí, 45")
        .com_preco(90)
        .com_fotos(["https://example.com/foto3.jpg"])
        .com_status("DISPONIVEL")
        .com_timezone("America/Sao_Paulo")
        .build(),

    # Espaços em São Paulo
    SpaceBuilder("s3", "Quadra Central SP")
        .com_esporte("Basquete")
        .com_localizacao("São Paulo")
        .com_preco(150)
        .com_fotos(["https://example.com/foto4.jpg"])
        .com_status("DISPONIVEL")
        .com_timezone("America/Sao_Paulo")
        .build(),

    SpaceBuilder("s4", "Piscina Olímpica")
        .com_esporte("Natação")
        .com_localizacao("São Paulo")
        .com_preco(200)
        .com_fotos(["https://example.com/foto5.jpg", "https://example.com/foto6.jpg"])
        .com_status("DISPONIVEL")
        .com_timezone("America/Sao_Paulo")
        .build(),

    # Espaço em manutenção
    SpaceBuilder("s5", "Quadra de Tênis")
        .com_esporte("Tênis")
        .com_localizacao("Farol, Maceió - AL, Rua Santa Luzia, 220")
        .com_preco(100)
        .com_fotos(["https://example.com/foto7.jpg"])
        .com_status("MANUTENCAO")
        .com_timezone("America/Sao_Paulo")
        .build(),
]

# ============ INTERVALOS DE TEMPO SIMULADOS ============
base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

mock_slots = [
    # Intervalos para Arena Pajuçara (s1)
    TimeSlot(
        "t1",
        "s1",
        base_date.replace(hour=18),
        base_date.replace(hour=19),
        "DISPONIVEL"
    ),
    TimeSlot(
        "t2",
        "s1",
        base_date.replace(hour=19),
        base_date.replace(hour=20),
        "DISPONIVEL"
    ),
    TimeSlot(
        "t3",
        "s1",
        base_date.replace(hour=20),
        base_date.replace(hour=21),
        "RESERVADO"
    ),
    # Slots for Quadra Jatiúca (s2)
    TimeSlot(
        "t4",
        "s2",
        base_date.replace(hour=17),
        base_date.replace(hour=18),
        "DISPONIVEL"
    ),
    TimeSlot(
        "t5",
        "s2",
        base_date.replace(hour=18),
        base_date.replace(hour=19),
        "DISPONIVEL"
    ),
    # Slots for Quadra Central SP (s3)
    TimeSlot(
        "t6",
        "s3",
        base_date.replace(hour=19),
        base_date.replace(hour=20),
        "DISPONIVEL"
    ),
    TimeSlot(
        "t7",
        "s3",
        base_date.replace(hour=20),
        base_date.replace(hour=21),
        "BLOQUEADO"
    ),
]

# ============ MOCK BOOKINGS ============
mock_bookings = [
    Booking(
        "bk1",
        "u2",
        "s1",
        "t1",
        "CONFIRMADO",
        120,
        0
    ),
    Booking(
        "bk2",
        "u3",
        "s2",
        "t4",
        "RESERVADO",
        90,
        0
    ),
    Booking(
        "bk3",
        "u1",
        "s3",
        "t6",
        "CONFIRMADO",
        150,
        0
    ),
]

# ============ MOCK NOTIFICATIONS ============
mock_notifications = [
    Notification(
        "n1",
        "u2",
        "Confirmação de Reserva",
        "Sua reserva na Arena Pajuçara foi confirmada!",
        "EMAIL",
        "ENVIADA"
    ),
    Notification(
        "n2",
        "u3",
        "Lembrete de Reserva",
        "Sua reserva está agendada para amanhã!",
        "SMS",
        "PENDENTE"
    ),
    Notification(
        "n3",
        "u1",
        "Notificação de Cancelamento",
        "Sua reserva foi cancelada.",
        "PUSH",
        "FALHA"
    ),
]
