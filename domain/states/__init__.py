"""States module — State Pattern para Booking e Notification"""
from .booking_states import (
    EstadoBooking,
    EstadoReservado,
    EstadoConfirmado,
    EstadoCheckinRealizado,
    EstadoCancelado,
    EstadoNaoCompareceu,
    EstadoReembolsado,
    ESTADOS_BOOKING,
)
from .notification_states import (
    EstadoNotification,
    EstadoPendente,
    EstadoEnviada,
    EstadoLida,
    EstadoFalha,
    ESTADOS_NOTIFICATION,
)
