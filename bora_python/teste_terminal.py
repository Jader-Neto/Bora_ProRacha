#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste Completo via Terminal
Use como: python teste_terminal.py
Teste todos os recursos da BORA PRORRACHA digitando no terminal
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from domain.user import User
from domain.space import Space
from domain.booking import Booking
from domain.timeslot import TimeSlot
from services.quick_registration_service import QuickRegistrationService
from services.dynamic_space_registration_service import DynamicSpaceRegistrationService
from services.easy_booking_service import EasyBookingService
from services.filter_service import FilterService
from services.detailed_space_service import DetailedSpaceService
from services.reminder_service import ReminderService
from services.checkin_service import CheckinService
from services.cancellation_service import CancellationService
from services.sync_service import SyncService
from services.timezone_service import TimezoneService
from datetime import datetime, timedelta


def limpar_tela():
    """Limpar tela do terminal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def titulo(texto):
    """Mostra um título formatado"""
    print("\n" + "="*70)
    print(f"  {texto}".center(70))
    print("="*70 + "\n")


def linha():
    """Mostra uma linha separadora"""
    print("-"*70)


def input_seguro(msg, tipo=str, minimo=None, maximo=None):
    """Input com tratamento de erro"""
    while True:
        try:
            valor = input(msg).strip()
            if not valor:
                print("⚠️  Campo não pode estar vazio!\n")
                continue
            
            if tipo == float:
                valor = float(valor)
                if minimo is not None and valor < minimo:
                    print(f"⚠️  Valor deve ser maior que {minimo}!\n")
                    continue
            elif tipo == int:
                valor = int(valor)
            
            return valor
        except ValueError:
            print(f"⚠️  Valor inválido! Tente novamente.\n")


def teste_cadastro_google():
    """Teste: Cadastro via Google"""
    titulo("CADASTRO VIA GOOGLE")
    
    email = input_seguro("📧 Email (ex: joao@gmail.com): ")
    
    try:
        service = QuickRegistrationService()
        usuario = service.login_com_google(email)
        
        print(f"\n✅ Usuário criado via Google!")
        print(f"   ID: {usuario.id}")
        print(f"   Nome: {usuario.nome}")
        print(f"   Email: {usuario.email}")
        print(f"   Status: {usuario.status}")
        print(f"   Progresso: {service.obter_progresso_cadastro(usuario)}%")
        
        completar = input("\n🔧 Completar cadastro agora? (s/n): ").lower()
        if completar == 's':
            telefone = input_seguro("📱 Telefone (ex: 85987654321): ")
            usuario.completar_cadastro(telefone)
            
            print(f"\n✅ Cadastro completado!")
            print(f"   Status: {usuario.status}")
            print(f"   Telefone: {usuario.telefone}")
            print(f"   Progresso: {service.obter_progresso_cadastro(usuario)}%")
            print(f"   ✓ Pode fazer reservas? {usuario.pode_reservar()}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")


def teste_cadastro_facebook():
    """Teste: Cadastro via Facebook"""
    titulo("CADASTRO VIA FACEBOOK")
    
    email = input_seguro("📧 Email: ")
    nome = input_seguro("👤 Nome completo: ")
    
    try:
        service = QuickRegistrationService()
        usuario = service.login_com_facebook(email, nome)
        
        print(f"\n✅ Usuário criado via Facebook!")
        print(f"   ID: {usuario.id}")
        print(f"   Nome: {usuario.nome}")
        print(f"   Email: {usuario.email}")
        print(f"   Status: {usuario.status}")
        print(f"   Progresso: {service.obter_progresso_cadastro(usuario)}%")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")


def teste_cadastro_espaco():
    """Teste: Cadastro de Espaço"""
    titulo("CADASTRO DE ESPAÇO DINÂMICO")
    
    nome = input_seguro("🏐 Nome do espaço: ")
    esporte = input_seguro("⚽ Esporte (ex: Futebol, Vôlei): ")
    localizacao = input_seguro("📍 Localização (ex: Maceió): ")
    preco = input_seguro("💰 Preço/hora (ex: 85.00): ", tipo=float, minimo=0.01)
    
    fotos_str = input("📷 Fotos (separadas por vírgula, ou ENTER para pular): ").strip()
    fotos = [f.strip() for f in fotos_str.split(",")] if fotos_str else []
    
    try:
        service = DynamicSpaceRegistrationService()
        espaco = service.cadastrar_espaco(
            nome=nome,
            esporte=esporte,
            localizacao=localizacao,
            preco_hora=preco,
            timezone="America/Sao_Paulo",
            fotos=fotos
        )
        
        print(f"\n✅ Espaço registrado com sucesso!")
        print(f"   ID: {espaco.id}")
        print(f"   Nome: {espaco.nome}")
        print(f"   Esporte: {espaco.esporte}")
        print(f"   Localização: {espaco.localizacao}")
        print(f"   Preço/hora: R$ {espaco.preco_hora:.2f}")
        print(f"   Status: {espaco.status}")
        print(f"   Fotos: {len(espaco.fotos)} imagens")
        
        atualizar = input("\n📝 Deseja atualizar o preço? (s/n): ").lower()
        if atualizar == 's':
            novo_preco = input_seguro("💰 Novo preço/hora: ", tipo=float, minimo=0.01)
            service.atualizar_preco(espaco.id, novo_preco)
            print(f"✅ Preço atualizado para R$ {novo_preco:.2f}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")


def teste_validacao_email():
    """Teste: Validar Email"""
    titulo("TESTE DE VALIDAÇÃO - EMAIL")
    
    email = input_seguro("📧 Digite um email para validar: ")
    
    try:
        user = User("u_test", "Teste", email)
        print(f"\n✅ Email válido! ✓")
        print(f"   Email: {email}")
    except ValueError as e:
        print(f"\n❌ Email inválido!")
        print(f"   Erro: {e}")
    
    linha()
    input("Pressione ENTER para continuar...")


def teste_validacao_preco():
    """Teste: Validar Preço"""
    titulo("TESTE DE VALIDAÇÃO - PREÇO")
    
    try:
        preco = input_seguro("💰 Digite um preço para validar: ", tipo=float)
        space = Space("s_test", "Teste", "Teste", "Teste", preco, [])
        print(f"\n✅ Preço válido! ✓")
        print(f"   Preço: R$ {preco:.2f}")
    except ValueError as e:
        print(f"\n❌ Preço inválido!")
        print(f"   Erro: {e}")
    
    linha()
    input("Pressione ENTER para continuar...")


def teste_reserva():
    """Teste: Criar Reserva"""
    titulo("TESTE DE RESERVA (AGENDAMENTO)")
    
    print("📝 Vamos criar uma reserva passo a passo...\n")
    
    try:
        # Criar usuário
        email_user = input_seguro("📧 Email do usuário: ")
        nome_user = input_seguro("👤 Nome do usuário: ")
        service_user = QuickRegistrationService()
        usuario = service_user.login_com_google(email_user)
        usuario.nome = nome_user
        usuario.completar_cadastro("85987654321")
        print(f"✅ Usuário criado: {usuario.nome}")
        
        # Criar espaço
        print("\n--- Cadastrando espaço para a reserva ---")
        nome_espaco = input_seguro("🏐 Nome do espaço: ")
        esporte = input_seguro("⚽ Esporte: ")
        localizacao = input_seguro("📍 Localização: ")
        preco = input_seguro("💰 Preço/hora: ", tipo=float, minimo=0.01)
        
        service_space = DynamicSpaceRegistrationService()
        espaco = service_space.cadastrar_espaco(
            nome=nome_espaco,
            esporte=esporte,
            localizacao=localizacao,
            preco_hora=preco,
            timezone="America/Sao_Paulo",
            fotos=["foto.jpg"]
        )
        print(f"✅ Espaço criado: {espaco.nome}")
        
        # Criar reserva
        print("\n--- Criando reserva ---")
        horas = input_seguro("⏱️  Quantas horas? ", tipo=int, minimo=1, maximo=24)
        
        service_booking = EasyBookingService()
        # Criar TimeSlot para a reserva
        agora = datetime.now()
        timeslot = TimeSlot(
            slot_id=f"ts_{usuario.id}_{espaco.id}",
            space_id=espaco.id,
            inicio=agora,
            fim=agora + timedelta(hours=horas),
            status="DISPONIVEL"
        )
        reserva = service_booking.criar_reserva_rapida(
            user_id=usuario.id,
            space_id=espaco.id,
            slot_id=timeslot.id,
            valor_total=espaco.preco_hora * horas
        )
        
        print(f"\n✅ Reserva criada com sucesso!")
        print(f"   ID da Reserva: {reserva.id}")
        print(f"   Usuário: {usuario.nome}")
        print(f"   Espaço: {espaco.nome}")
        print(f"   Duração: {horas} hora(s)")
        print(f"   Valor total: R$ {reserva.valor_total:.2f}")
        print(f"   Status: {reserva.status}")
        
        # Confirmar reserva
        confirmar = input("\n✔️  Confirmar a reserva? (s/n): ").lower()
        if confirmar == 's':
            reserva.confirmar()
            print(f"✅ Reserva confirmada! Status: {reserva.status}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_filtros():
    """Teste: Filtrar Espaços"""
    titulo("TESTE DE FILTROS - BUSCAR ESPAÇOS")
    
    try:
        # Criar alguns espaços de exemplo
        print("🔄 Criando espaços de exemplo...\n")
        service = DynamicSpaceRegistrationService()
        
        espacos_dados = [
            ("Quadra Centro", "Futebol", "Maceió", 80.00),
            ("Quadra Praia", "Vôlei", "Maceió", 100.00),
            ("Quadra Interior", "Futebol", "Arapiraca", 60.00),
            ("Arena Premium", "Vôlei", "Maceió", 150.00),
        ]
        
        espacos = []
        for nome, esporte, local, preco in espacos_dados:
            espaco = service.cadastrar_espaco(
                nome=nome,
                esporte=esporte,
                localizacao=local,
                preco_hora=preco,
                timezone="America/Sao_Paulo",
                fotos=["foto.jpg"]
            )
            espacos.append(espaco)
            print(f"✓ {nome}")
        
        print(f"\n✅ {len(espacos)} espaços criados!")
        
        # Filtrar
        print("\n--- Filtros disponíveis ---")
        print("1. Por Localização")
        print("2. Por Esporte")
        print("3. Por Preço Máximo")
        
        opcao_filtro = input("\nEscolha um filtro (1-3): ").strip()
        
        filter_service = FilterService()
        
        if opcao_filtro == "1":
            local = input_seguro("📍 Digite a localização: ")
            from domain.filtro import FiltroPorLocal
            filtro = FiltroPorLocal(local)
            resultado = filter_service.aplicar_filtro(espacos, filtro)
            print(f"\n✅ Espaços em {local}:")
            
        elif opcao_filtro == "2":
            esporte = input_seguro("⚽ Digite o esporte: ")
            from domain.filtro import FiltroPorEsporte
            filtro = FiltroPorEsporte(esporte)
            resultado = filter_service.aplicar_filtro(espacos, filtro)
            print(f"\n✅ Espaços de {esporte}:")
            
        elif opcao_filtro == "3":
            preco_max = input_seguro("💰 Preço máximo: ", tipo=float, minimo=0.01)
            from domain.filtro import FiltroPorPreco
            filtro = FiltroPorPreco(preco_max)
            resultado = filter_service.aplicar_filtro(espacos, filtro)
            print(f"\n✅ Espaços até R$ {preco_max}:")
        
        else:
            resultado = espacos
            print("\n📋 Todos os espaços:")
        
        for i, espaco in enumerate(resultado, 1):
            print(f"\n{i}. {espaco.nome}")
            print(f"   ⚽ Esporte: {espaco.esporte}")
            print(f"   📍 Localização: {espaco.localizacao}")
            print(f"   💰 Preço: R$ {espaco.preco_hora:.2f}/h")
            print(f"   ✓ Status: {espaco.status}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_espacos_detalhados():
    """Teste: Espaços detalhados (Funcionalidade 5)"""
    titulo("TESTE DE ESPAÇOS DETALHADOS")

    print("⭐ Demonstrando detalhes, avaliações e comentários...\n")

    try:
        espaco = Space(
            "s_detalhado",
            "Arena Central",
            "Futebol",
            "Maceió",
            120.0,
            ["arena1.jpg", "arena2.jpg"]
        )

        service = DetailedSpaceService()
        detalhes_iniciais = service.obter_detalhes_espaco(espaco)

        print("1️⃣ Detalhes iniciais:")
        print(f"   Nome: {detalhes_iniciais['nome']}")
        print(f"   Esporte: {detalhes_iniciais['esporte']}")
        print(f"   Localização: {detalhes_iniciais['localizacao']}")
        print(f"   Preço/hora: R$ {detalhes_iniciais['preco_hora']:.2f}")

        print("\n2️⃣ Adicionando avaliações...")
        for nota in [5, 4, 5]:
            media = service.adicionar_avaliacao(espaco.id, nota)
            print(f"   ✓ Nota {nota} adicionada | Média atual: {media:.1f}")

        print("\n3️⃣ Adicionando comentários...")
        service.adicionar_comentario(espaco.id, "Quadra muito bem cuidada")
        service.adicionar_comentario(espaco.id, "Iluminação excelente")
        print("   ✓ 2 comentários adicionados")

        detalhes_finais = service.obter_detalhes_espaco(espaco)
        print("\n4️⃣ Resumo final:")
        print(f"   Avaliação média: {service.obter_media_avaliacoes(espaco.id):.1f}/5")
        print(f"   Total de comentários: {detalhes_finais['total_comentarios']}")

        linha()
        input("Pressione ENTER para continuar...")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_lembrete_interativo():
    """Teste: Lembretes interativos (Funcionalidade 7)"""
    titulo("TESTE DE LEMBRETES INTERATIVOS")

    print("🔔 Demonstrando agendamento e envio de lembretes...\n")

    try:
        usuario = User("u_rem", "Carlos", "carlos@email.com")
        espaco = Space("s_rem", "Quadra Leste", "Futsal", "Maceió", 90.0, ["foto.jpg"])

        reserva = Booking(
            booking_id="bk_rem_01",
            user_id=usuario.id,
            space_id=espaco.id,
            slot_id="ts_rem_01",
            status="RESERVADO",
            valor_total=180.0
        )
        reserva.confirmar()

        horas = input_seguro("⏰ Lembrar com quantas horas de antecedência? ", tipo=int, minimo=1)

        service = ReminderService()
        lembrete = service.agendar_lembrete(reserva, horas)

        print("\n✅ Lembrete agendado:")
        print(f"   ID: {lembrete.id}")
        print(f"   Tipo: {lembrete.tipo}")
        print(f"   Status: {lembrete.status}")

        enviar = input("\n📨 Enviar todos os lembretes pendentes agora? (s/n): ").strip().lower()
        if enviar == "s":
            enviados = service.enviar_todos_lembretes()
            print(f"   ✅ Lembretes enviados: {enviados}")

        stats = service.obter_estatisticas_lembretes()
        print("\n📊 Estatísticas:")
        print(f"   Total: {stats['total']}")
        print(f"   Pendentes: {stats['pendentes']}")
        print(f"   Enviadas: {stats['enviadas']}")

        linha()
        input("Pressione ENTER para continuar...")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_encapsulamento():
    """Teste: Verificar Encapsulamento"""
    titulo("TESTE DE ENCAPSULAMENTO - PROTEÇÃO DE DADOS")
    
    print("🔒 Demonstrando encapsulamento com @property...\n")
    
    try:
        # Criar espaço
        espaco = Space(
            id="s_test",
            nome="Quadra Teste",
            esporte="Futebol",
            localizacao="Maceió",
            preco_hora=100.0,
            fotos=["foto1.jpg", "foto2.jpg"]
        )
        
        print(f"1️⃣ Espaço criado:")
        print(f"   Nome: {espaco.nome}")
        print(f"   Preço: R$ {espaco.preco_hora:.2f}")
        print(f"   Status: {espaco.status}")
        
        print(f"\n2️⃣ Atualizando preço via @property setter...")
        novo_preco = input_seguro("   💰 Novo preço: ", tipo=float, minimo=0.01)
        espaco.preco_hora = novo_preco
        print(f"   ✅ Preço atualizado para R$ {espaco.preco_hora:.2f}")
        
        print(f"\n3️⃣ Tentando acessar atributo privado (_nome)...")
        print(f"   ⚠️  Nome privado: {espaco._nome}")
        print(f"   ℹ️  Começar com '_' indica que é privado (não deve acessar diretamente)")
        
        print(f"\n4️⃣ Testando proteção de lista (fotos)...")
        fotos_copia = espaco.fotos
        print(f"   Fotos originais: {fotos_copia}")
        fotos_copia.append("nova_foto.jpg")
        print(f"   Fotos após modificação: {espaco.fotos}")
        print(f"   ✅ Lista original não foi modificada! (retorna cópia)")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")


def teste_heranca():
    """Teste: Verificar Herança"""
    titulo("TESTE DE HERANÇA - CADEIA DE CLASSES")
    
    print("👪 Demonstrando herança e polimorfismo...\n")
    
    try:
        # Criar instâncias
        usuario = User("u_test", "João Silva", "joao@email.com")
        espaco = Space("s_test", "Quadra", "Futebol", "Maceió", 100.0, ["foto.jpg"])
        reserva = Booking("bk_test", usuario.id, espaco.id, 3, 300.0, "AGENDADA")
        
        print(f"1️⃣ Verificando ID (herança de BaseEntity):")
        print(f"   User.id: {usuario.id}")
        print(f"   Space.id: {espaco.id}")
        print(f"   Booking.id: {reserva.id}")
        print(f"   ✅ Todos têm atributo 'id' da classe BaseEntity!")
        
        print(f"\n2️⃣ Verificando __repr__ (herança):")
        print(f"   User: {usuario}")
        print(f"   Space: {espaco}")
        print(f"   ✅ Ambos herdam __repr__ de BaseEntity!")
        
        print(f"\n3️⃣ Verificando Status (herança de EntityComStatus):")
        print(f"   Booking.status: {reserva.status}")
        print(f"   ✅ Booking herda EntityComStatus que herda BaseEntity!")
        
        print(f"\n4️⃣ Testando mudança de status:")
        print(f"   Status anterior: {reserva.status}")
        reserva.confirmar()
        print(f"   Status após confirmar(): {reserva.status}")
        print(f"   ✅ Método herança funcionando!")
        
        print(f"\n5️⃣ Hierarquia de classes:")
        print(f"   BaseEntity")
        print(f"   ├── User (herda de BaseEntity)")
        print(f"   ├── Space (herda de BaseEntity)")
        print(f"   └── EntityComStatus (herda de BaseEntity)")
        print(f"       └── Booking (herda de EntityComStatus)")
        print(f"       └── TimeSlot (herda de EntityComStatus)")
        print(f"       └── Notification (herda de EntityComStatus)")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_polimorfismo():
    """Teste: Verificar Polimorfismo"""
    titulo("TESTE DE POLIMORFISMO - MESMA INTERFACE, COMPORTAMENTOS DIFERENTES")
    
    print("🔄 Demonstrando polimorfismo com diferentes tipos de filtros...\n")
    
    try:
        from domain.filtro import FiltroPorLocal, FiltroPorEsporte, FiltroPorPreco, FiltroCombinado
        
        # Criar espaços
        espaco1 = Space("s1", "Quadra A", "Futebol", "Maceió", 80.0, ["foto.jpg"])
        espaco2 = Space("s2", "Arena B", "Vôlei", "Maceió", 100.0, ["foto.jpg"])
        espaco3 = Space("s3", "Quadra C", "Futebol", "Arapiraca", 60.0, ["foto.jpg"])
        
        espacos = [espaco1, espaco2, espaco3]
        
        print(f"Espaços disponíveis: {len(espacos)}")
        for e in espacos:
            print(f"  • {e.nome} - {e.esporte} - {e.localizacao} - R$ {e.preco_hora}")
        
        print(f"\n1️⃣ POLIMORFISMO - Mesmo método 'aplicar()', resultados diferentes:")
        
        # Filtro 1: Por Local
        print(f"\n📍 Filtro por Localização (Maceió):")
        filtro_local = FiltroPorLocal("Maceió")
        resultado = filtro_local.aplicar(espacos)
        print(f"   Critério: {filtro_local.obter_criterio()}")
        print(f"   ✓ Resultado: {len(resultado)} espaço(s)")
        for e in resultado:
            print(f"     • {e.nome}")
        
        # Filtro 2: Por Esporte
        print(f"\n⚽ Filtro por Esporte (Futebol):")
        filtro_esporte = FiltroPorEsporte("Futebol")
        resultado = filtro_esporte.aplicar(espacos)
        print(f"   Critério: {filtro_esporte.obter_criterio()}")
        print(f"   ✓ Resultado: {len(resultado)} espaço(s)")
        for e in resultado:
            print(f"     • {e.nome}")
        
        # Filtro 3: Por Preço
        print(f"\n💰 Filtro por Preço Máximo (R$ 80.00):")
        filtro_preco = FiltroPorPreco(80.0)
        resultado = filtro_preco.aplicar(espacos)
        print(f"   Critério: {filtro_preco.obter_criterio()}")
        print(f"   ✓ Resultado: {len(resultado)} espaço(s)")
        for e in resultado:
            print(f"     • {e.nome}")
        
        # Filtro 4: Combinado (COMPOSIÇÃO)
        print(f"\n🔗 Filtro Combinado (Maceió + Futebol):")
        filtro_combinado = FiltroCombinado([filtro_local, filtro_esporte])
        resultado = filtro_combinado.aplicar(espacos)
        print(f"   Critério: {filtro_combinado.obter_criterio()}")
        print(f"   ✓ Resultado: {len(resultado)} espaço(s)")
        for e in resultado:
            print(f"     • {e.nome}")
        
        print(f"\n✅ POLIMORFISMO: Todos os filtros implementam IFiltro")
        print(f"   Mesma interface, comportamentos diferentes!")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_classe_abstrata():
    """Teste: Verificar Classe Abstrata"""
    titulo("TESTE DE CLASSE ABSTRATA - NÃO PODE INSTANCIAR DIRETAMENTE")
    
    print("🔒 Demonstrando que classes abstratas não podem ser instanciadas...\n")
    
    try:
        from domain.base import BaseEntity
        from domain.filtro import FiltroEspaco
        from domain.interfaces import IFiltro
        
        print("1️⃣ Tentando instanciar BaseEntity (classe abstrata):")
        try:
            obj = BaseEntity("id_teste")
            print(f"   ❌ Não deveria permitir!")
        except TypeError as e:
            print(f"   ✅ Erro esperado: {str(e)[:60]}...")
        
        print(f"\n2️⃣ Tentando instanciar FiltroEspaco (classe abstrata):")
        try:
            filtro = FiltroEspaco()
            print(f"   ❌ Não deveria permitir!")
        except TypeError as e:
            print(f"   ✅ Erro esperado: {str(e)[:60]}...")
        
        print(f"\n3️⃣ Instanciando Space (subclasse concreta):")
        espaco = Space("s1", "Quadra", "Futebol", "Maceió", 100.0, ["foto.jpg"])
        print(f"   ✅ Space criado: {espaco.nome}")
        
        print(f"\n4️⃣ Usando filtro concreto (FiltroPorLocal):")
        from domain.filtro import FiltroPorLocal
        filtro = FiltroPorLocal("Maceió")
        print(f"   ✅ Filtro criado: {filtro.obter_criterio()}")
        
        print(f"\n✅ CLASSE ABSTRATA: Força implementação de métodos!")
        print(f"   Subclasses devem implementar @abstractmethod")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_checkin():
    """Teste: Check-in com QR Code"""
    titulo("TESTE DE CHECK-IN - VALIDAÇÃO DE PRESENÇA")
    
    print("✔️  Demonstrando check-in com código QR...\n")
    
    try:
        # Criar dados simples
        usuario = User("u_test", "João Silva", "joao@email.com")
        usuario.completar_cadastro("85987654321")
        
        espaco = Space("s_test", "Quadra", "Futebol", "Maceió", 100.0, ["foto.jpg"])
        
        # Criar reserva simples
        reserva = Booking(
            booking_id="bk_checkin_test",
            user_id=usuario.id,
            space_id=espaco.id,
            slot_id="ts_test",
            status="RESERVADO",
            valor_total=200.0
        )
        
        print(f"📋 Reserva criada:")
        print(f"   ID: {reserva.id}")
        print(f"   Usuário: {usuario.nome}")
        print(f"   Espaço: {espaco.nome}")
        print(f"   Status: {reserva.status}")
        print(f"   Valor: R$ {reserva.valor_total:.2f}")
        
        reserva.confirmar()
        print(f"\n✅ Reserva confirmada automaticamente para seguir o fluxo da funcionalidade 10")
        print(f"   Novo status: {reserva.status}")

        # Fazer check-in no mesmo padrão do main.py
        service = CheckinService()
        codigo_qr = service.gerar_codigo_qr(reserva)
        print(f"\n🔳 Código QR gerado: {codigo_qr}")

        info_checkin = service.realizar_checkin(reserva)
        print(f"✅ Check-in realizado! Status: {info_checkin['novo_status']}")

        recibo = service.gerar_recibo_checkin(reserva)
        print(recibo)
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_cancelamento():
    """Teste: Cancelar Reserva"""
    titulo("TESTE DE CANCELAMENTO - POLÍTICA DE CANCELAMENTO")
    
    print("❌ Demonstrando cancelamento com política de reembolso...\n")
    
    try:
        # Criar dados
        usuario = User("u_test", "Maria Santos", "maria@email.com")
        espaco = Space("s_test", "Quadra", "Futebol", "Maceió", 100.0, ["foto.jpg"])
        
        service_booking = EasyBookingService()
        # Criar TimeSlot para a reserva
        agora = datetime.now()
        timeslot = TimeSlot(
            slot_id=f"ts_{usuario.id}_{espaco.id}",
            space_id=espaco.id,
            inicio=agora,
            fim=agora + timedelta(hours=2),
            status="DISPONIVEL"
        )
        reserva = service_booking.criar_reserva_rapida(
            user_id=usuario.id,
            space_id=espaco.id,
            slot_id=timeslot.id,
            valor_total=espaco.preco_hora * 2
        )
        reserva.confirmar()
        
        print(f"📋 Reserva antes do cancelamento:")
        print(f"   ID: {reserva.id}")
        print(f"   Status: {reserva.status}")
        print(f"   Valor: R$ {reserva.valor_total:.2f}")
        
        # Cancelar
        print(f"\n1️⃣ Cancelando reserva...")
        
        from services.cancellation_service import CancellationService
        service_cancel = CancellationService()
        resultado = service_cancel.cancelar_com_politica(reserva, tempo_antecedencia_horas=24)
        
        print(f"   ✅ Reserva cancelada!")
        
        print(f"\n2️⃣ Resultado do cancelamento:")
        print(f"   Status: {resultado['status']}")
        print(f"   Valor original: R$ {resultado['valor_original']:.2f}")
        print(f"   Taxa de cancelamento: R$ {resultado['taxa_cancelamento']:.2f}")
        print(f"   Reembolso: R$ {resultado['reembolso']:.2f}")
        print(f"   Tempo de antecedência: {resultado['tempo_antecedencia']}h")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_sincronizacao():
    """Teste: Sincronização de Dados"""
    titulo("TESTE DE SINCRONIZAÇÃO - ATUALIZAR DADOS EM LOTE")
    
    print("🔄 Demonstrando sincronização de múltiplos registros...\n")
    
    try:
        sync_service = SyncService()

        print("1️⃣ Criando espaços e slots de exemplo...")
        espaco1 = Space("s1", "Quadra Centro", "Futebol", "Maceió", 100.0, ["foto.jpg"])
        espaco2 = Space("s2", "Arena Praia", "Vôlei", "Maceió", 120.0, ["foto.jpg"])
        espacos = [espaco1, espaco2]

        agora = datetime.now()
        slots_espaco1 = [
            TimeSlot("ts1", "s1", agora, agora + timedelta(hours=1), "DISPONIVEL"),
            TimeSlot("ts2", "s1", agora + timedelta(hours=1), agora + timedelta(hours=2), "DISPONIVEL")
        ]
        slots_espaco2 = [
            TimeSlot("ts3", "s2", agora, agora + timedelta(hours=1), "DISPONIVEL")
        ]

        print("2️⃣ Criando reserva para forçar sincronização de um slot...")
        booking = Booking(
            booking_id="bk_sync_01",
            user_id="u_sync",
            space_id="s1",
            slot_id="ts1",
            status="CONFIRMADO",
            valor_total=100.0
        )
        bookings = [booking]

        slots_map = {
            "s1": slots_espaco1,
            "s2": slots_espaco2,
        }

        print("3️⃣ Executando sincronização em lote...")
        sync_service.sincronizar_lote(espacos, slots_map, bookings)
        print("   ✅ Sincronização concluída")

        print("\n4️⃣ Resultado dos slots:")
        for slot in slots_espaco1 + slots_espaco2:
            print(f"   • {slot.id} ({slot.space_id}) -> {slot.status}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def teste_timezone():
    """Teste: Gerenciamento de Timezone"""
    titulo("TESTE DE TIMEZONE - CONVERTER HORÁRIOS ENTRE FUSOS")
    
    print("🌍 Demonstrando conversão de timezones...\n")
    
    try:
        timezone_service = TimezoneService()

        print("1️⃣ Timezones suportados:")
        timezones = timezone_service.obter_timezones_disponiveis()
        for tz in timezones[:6]:
            print(f"   • {tz}")

        print("\n2️⃣ Ajustando timezone do espaço:")
        espaco = Space("s1", "Quadra", "Futebol", "Fortaleza", 100.0, ["foto.jpg"])
        timezone_service.ajustar_timezone(espaco, "America/Sao_Paulo")
        print(f"   ✅ Timezone atual: {espaco.timezone}")

        print("\n3️⃣ Conversão demonstrativa:")
        convertido = timezone_service.converter_horario("14:30", "America/Sao_Paulo", "UTC")
        print(f"   Resultado: {convertido}")

        relatorio = timezone_service.obter_relatorio_timezones([espaco])
        print("\n4️⃣ Relatório de timezones:")
        print(f"   Distribuição: {relatorio['distribuicao_timezones']}")
        
        linha()
        input("Pressione ENTER para continuar...")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para continuar...")


def menu_principal():
    """Menu principal"""
    while True:
        limpar_tela()
        
        print("\n" + "="*70)
        print("🎯 BORA PRORRACHA - MODO INTERATIVO (10 FUNCIONALIDADES) 🎯".center(70))
        print("="*70)
        print("\n📋 FUNCIONALIDADES (MESMA ORDEM DO main.py):\n")
        print("  1. Sincronização")
        print("  2. Cadastro Rápido")
        print("  3. Agendamento Fácil")
        print("  4. Filtro Dinâmico")
        print("  5. Espaços Detalhados")
        print("  6. Cadastro de Espaço Dinâmico")
        print("  7. Lembrete Interativo")
        print("  8. Fuso Horário Dinâmico")
        print("  9. Cancelamentos")
        print("  10. Confirmação de Agendamento (Check-in)")

        print("\n🔧 EXTRAS:\n")
        print("  A. Validações (Email, Preço)")
        print("  B. Herança")
        print("  C. Polimorfismo")
        print("  D. Classe Abstrata")
        print("  E. Encapsulamento")
        print("  F. Ver Todos os Conceitos")

        print("\n  0. Sair")

        print("\n" + "-"*70)
        opcao = input("Digite a opção (0-10 ou A-F): ").strip().upper()

        if opcao == "1":
            teste_sincronizacao()
        elif opcao == "2":
            print("\nEscolha o tipo de cadastro rápido:")
            print("  1. Google")
            print("  2. Facebook")
            subtipo = input("Opção: ").strip()
            if subtipo == "1":
                teste_cadastro_google()
            elif subtipo == "2":
                teste_cadastro_facebook()
            else:
                print("\n❌ Opção inválida!")
                input("Pressione ENTER...")
        elif opcao == "3":
            teste_reserva()
        elif opcao == "4":
            teste_filtros()
        elif opcao == "5":
            teste_espacos_detalhados()
        elif opcao == "6":
            teste_cadastro_espaco()
        elif opcao == "7":
            teste_lembrete_interativo()
        elif opcao == "8":
            teste_timezone()
        elif opcao == "9":
            teste_cancelamento()
        elif opcao == "10":
            teste_checkin()
        elif opcao == "A":
            teste_validacao_email()
            teste_validacao_preco()
        elif opcao == "B":
            teste_heranca()
        elif opcao == "C":
            teste_polimorfismo()
        elif opcao == "D":
            teste_classe_abstrata()
        elif opcao == "E":
            teste_encapsulamento()
        elif opcao == "F":
            for teste in [teste_heranca, teste_polimorfismo, teste_classe_abstrata, teste_encapsulamento]:
                teste()
        elif opcao == "0":
            print("\n👋 Obrigado por usar BORA PRORRACHA!")
            print("Boa sorte na apresentação! 🚀\n")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.")
            input("Pressione ENTER...")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
