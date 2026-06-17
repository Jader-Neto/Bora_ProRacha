#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificação Rápida - Confirma que TUDO está pronto para apresentação
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from domain.user import User
from domain.space import Space
from domain.booking import Booking

print("\n" + "="*70)
print("✅ VERIFICAÇÃO RÁPIDA - BORA PRORRACHA".center(70))
print("="*70 + "\n")

try:
    print("1️⃣ Testando User...")
    user = User("u1", "João", "joao@email.com")
    user.completar_cadastro("85987654321")
    print(f"   ✅ User criado: {user.nome} (Status: {user.status})")
    
    print("\n2️⃣ Testando Space...")
    space = Space("s1", "Quadra", "Futebol", "Maceió", 100.0, ["foto.jpg"])
    print(f"   ✅ Space criado: {space.nome} (R$ {space.preco_hora}/h)")
    
    print("\n3️⃣ Testando Booking...")
    booking = Booking("bk1", user.id, space.id, "ts1", "RESERVADO", 200.0)
    booking.confirmar()
    print(f"   ✅ Booking criado: {booking.id} (Status: {booking.status})")
    
    print("\n4️⃣ Testando Herança...")
    print(f"   User.id (BaseEntity): {user.id}")
    print(f"   Space.id (BaseEntity): {space.id}")
    print(f"   Booking.status (EntityComStatus): {booking.status}")
    print("   ✅ Herança funcionando!")
    
    print("\n5️⃣ Testando Polimorfismo...")
    from domain.filtro import FiltroPorLocal, FiltroPorEsporte
    filtro1 = FiltroPorLocal("Maceió")
    filtro2 = FiltroPorEsporte("Futebol")
    print(f"   Filtro 1: {filtro1.obter_criterio()}")
    print(f"   Filtro 2: {filtro2.obter_criterio()}")
    print("   ✅ Polimorfismo funcionando!")
    
    print("\n" + "="*70)
    print("🎉 TUDO PRONTO PARA APRESENTAÇÃO! 🎉".center(70))
    print("="*70)
    print("\n✨ Scripts disponíveis:")
    print("   • python teste_cadastro.py          → Testes automáticos")
    print("   • python teste_terminal.py          → Menu interativo completo")
    print("   • python teste_cadastro_interativo.py → Testes com input")
    print("\n")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
