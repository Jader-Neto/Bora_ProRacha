"""
SyncService - Funcionalidade 1: Sincronização

Concito: Sincronização de agendas de espaços de esportes
Propósito: Evitar conflitos de agendamento e mostrar disponibilidade real
"""
from typing import List, Dict

from domain.space import Space
from domain.timeslot import TimeSlot
from domain.booking import Booking
from services.base import BaseService


class SyncService(BaseService):
    """Serviço de sincronização"""

    def __init__(self):
        super().__init__("SyncService")

    def sincronizar_espaco(
        self,
        space: Space,
        slots: List[TimeSlot],
        bookings: List[Booking]
    ) -> int:
        """
        Sincroniza um espaço com seus períodos de tempo
        
        Args:
            space: Espaço a sincronizar
            slots: Lista de períodos de tempo para o espaço
            bookings: Reservas existentes
            
        Returns:
            Número de períodos sincronizados
        """
        self.validar_string(space.id, "Space ID")

        sincronizados = 0

        for slot in slots:
            tem_booking = any(
                b.slot_id == slot.id and b.status != "CANCELADO"
                for b in bookings
            )

            # Sincroniza estado do período com estado do espaço
            if space.status == "MANUTENCAO":
                if slot.status != "BLOQUEADO":
                    slot.bloquear()
                    sincronizados += 1
            elif tem_booking and slot.status != "RESERVADO":
                slot.reservar()
                sincronizados += 1
            elif not tem_booking and slot.status == "RESERVADO":
                slot.cancelar()
                sincronizados += 1

        self.log(f"Espaço {space.nome} sincronizado: {sincronizados} período(s) atualizado(s)")
        return sincronizados

    def sincronizar_lote(
        self,
        spaces: List[Space],
        slots_map: Dict[str, List[TimeSlot]],
        bookings: List[Booking]
    ) -> None:
        """
        Sincroniza múltiplos espaços em lote

        Args:
            spaces: Lista de espaços
            slots_map: Mapa de períodos por espaço
            bookings: Todas as reservas
        """
        if not spaces or len(spaces) == 0:
            self.aviso("Nenhum espaço para sincronizar")
            return

        total_sincronizados = 0

        for space in spaces:
            slots = slots_map.get(space.id, [])
            total_sincronizados += self.sincronizar_espaco(space, slots, bookings)

        self.log(f"Sincronização em lote concluída: {total_sincronizados} períodos atualizados")

    def obter_disponibilidade(self, space: Space) -> int:
        """Obtém número de períodos disponíveis para um espaço"""
        return 1  # Espaço reservado, depende de dados externos
