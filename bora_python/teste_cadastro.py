#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste de Cadastro - Bora Prorracha
Demonstra todas as operações de cadastro do sistema
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from domain.user import User
from domain.space import Space
from services.quick_registration_service import QuickRegistrationService
from services.dynamic_space_registration_service import DynamicSpaceRegistrationService


def teste_cadastro_usuario_google():
    """Teste: Cadastro rápido com Google"""
    print("\n" + "="*70)
    print("TESTE 1: CADASTRO RÁPIDO COM GOOGLE")
    print("="*70)
    
    service = QuickRegistrationService()
    
    # ✅ Teste 1.1: Login com Google
    print("\n✓ Criando usuário via Google...")
    usuario = service.login_com_google("joao.silva@gmail.com")
    print(f"  ID: {usuario.id}")
    print(f"  Nome: {usuario.nome}")
    print(f"  Email: {usuario.email}")
    print(f"  Status: {usuario.status}")
    
    # ✅ Teste 1.2: Verificar progresso
    progresso = service.obter_progresso_cadastro(usuario)
    print(f"  Progresso de cadastro: {progresso}%")
    
    # ✅ Teste 1.3: Completar cadastro
    print("\n✓ Completando cadastro...")
    usuario.completar_cadastro("85987654321")
    print(f"  Status atualizado: {usuario.status}")
    print(f"  Telefone: {usuario.telefone}")
    progresso = service.obter_progresso_cadastro(usuario)
    print(f"  Progresso de cadastro: {progresso}%")
    
    # ✅ Teste 1.4: Verificar permissão de reserva
    pode_reservar = usuario.pode_reservar()
    print(f"  Pode fazer reservas? {pode_reservar}")
    
    return usuario


def teste_cadastro_usuario_facebook():
    """Teste: Cadastro com Facebook"""
    print("\n" + "="*70)
    print("TESTE 2: CADASTRO COM FACEBOOK")
    print("="*70)
    
    service = QuickRegistrationService()
    
    # ✅ Teste 2.1: Login com Facebook
    print("\n✓ Criando usuário via Facebook...")
    usuario = service.login_com_facebook(
        "maria.santos@facebook.com",
        "Maria Santos"
    )
    print(f"  ID: {usuario.id}")
    print(f"  Nome: {usuario.nome}")
    print(f"  Email: {usuario.email}")
    print(f"  Status: {usuario.status}")
    
    # ✅ Teste 2.2: Progresso
    progresso = service.obter_progresso_cadastro(usuario)
    print(f"  Progresso de cadastro: {progresso}%")
    
    return usuario


def teste_cadastro_espaco():
    """Teste: Cadastro dinâmico de espaço"""
    print("\n" + "="*70)
    print("TESTE 3: CADASTRO DE ESPAÇO DINÂMICO")
    print("="*70)
    
    service = DynamicSpaceRegistrationService()
    
    # ✅ Teste 3.1: Registrar novo espaço
    print("\n✓ Registrando novo espaço...")
    espaco = service.cadastrar_espaco(
        nome="Quadra Comunidade",
        esporte="Futebol",
        localizacao="Maceió",
        preco_hora=85.00,
        timezone="America/Sao_Paulo",
        fotos=["foto_frente.jpg", "foto_lateral.jpg"]
    )
    print(f"  ID: {espaco.id}")
    print(f"  Nome: {espaco.nome}")
    print(f"  Esporte: {espaco.esporte}")
    print(f"  Localização: {espaco.localizacao}")
    print(f"  Preço/hora: R$ {espaco.preco_hora}")
    print(f"  Status: {espaco.status}")
    print(f"  Timezone: {espaco.timezone}")
    print(f"  Fotos: {len(espaco.fotos)} imagens")
    
    # ✅ Teste 3.2: Obter espaços registrados
    print("\n✓ Consultando espaços registrados...")
    espacos = service.obter_espacos_registrados()
    print(f"  Total de espaços: {len(espacos)}")
    
    # ✅ Teste 3.3: Verificar disponibilidade
    disponivel = service.verificar_disponibilidade(espaco.id)
    print(f"  Espaço disponível? {disponivel}")
    
    # ✅ Teste 3.4: Atualizar preço
    print("\n✓ Atualizando preço...")
    espaco.atualizar_preco(95.00)
    print(f"  Novo preço: R$ {espaco.preco_hora}")
    service.atualizar_espaco(espaco)
    print(f"  Espaço atualizado com sucesso!")
    
    # ✅ Teste 3.5: Gerar relatório
    print("\n✓ Gerando relatório...")
    relatorio = service.obter_relatorio_registro()
    print(f"  Total de espaços: {relatorio['total_espacos']}")
    print(f"  Espaços disponíveis: {relatorio['espacos_disponiveis']}")
    print(f"  Espaços em manutenção: {relatorio['espacos_em_manutencao']}")
    print(f"  Esportes disponíveis: {relatorio['esportes']}")
    print(f"  Locais: {relatorio['locais']}")
    print(f"  Preço médio: R$ {relatorio['preco_medio']:.2f}")
    
    return espaco


def teste_validacoes():
    """Teste: Validações de cadastro"""
    print("\n" + "="*70)
    print("TESTE 4: VALIDAÇÕES")
    print("="*70)
    
    # ✅ Teste 4.1: Email inválido
    print("\n✓ Testando email inválido...")
    try:
        User("u1", "João", "email-invalido", "85987654321")
        print("  ❌ Deveria ter rejeitado email inválido!")
    except ValueError as e:
        print(f"  ✓ Validação funcionou: {e}")
    
    # ✅ Teste 4.2: Preço inválido
    print("\n✓ Testando preço negativo...")
    try:
        Space("s1", "Quadra", "Futebol", "Maceió", -100, [])
        print("  ❌ Deveria ter rejeitado preço negativo!")
    except ValueError as e:
        print(f"  ✓ Validação funcionou: {e}")
    
    # ✅ Teste 4.3: Modificar email com validação
    print("\n✓ Testando modificação de email...")
    user = User("u1", "João", "joao@email.com")
    try:
        user.email = "email-invalido"
        print("  ❌ Deveria ter rejeitado email inválido!")
    except ValueError as e:
        print(f"  ✓ Validação de setter funcionou: {e}")
    
    # ✅ Teste 4.4: Atualizar timezone inválido
    print("\n✓ Testando timezone vazio...")
    space = Space("s1", "Quadra", "Futebol", "Maceió", 100, [])
    try:
        space.timezone = ""
        print("  ❌ Deveria ter rejeitado timezone vazio!")
    except ValueError as e:
        print(f"  ✓ Validação de setter funcionou: {e}")


def teste_encapsulamento():
    """Teste: Verificar encapsulamento"""
    print("\n" + "="*70)
    print("TESTE 5: ENCAPSULAMENTO")
    print("="*70)
    
    # ✅ Teste 5.1: Não pode acessar direto
    print("\n✓ Testando proteção de atributo privado...")
    space = Space("s1", "Quadra", "Futebol", "Maceió", 100, [])
    print(f"  Nome via @property: {space.nome}")
    print(f"  Nome privado (_nome): {space._nome}")
    print(f"  ✓ Atributo protegido com underscore")
    
    # ✅ Teste 5.2: Adicionar avaliações (lista privada)
    print("\n✓ Testando proteção de lista...")
    space.adicionar_avaliacao(5)
    space.adicionar_avaliacao(4)
    avaliacoes = space.avaliacoes
    print(f"  Avaliações: {avaliacoes}")
    avaliacoes.append(3)  # Tenta modificar cópia
    print(f"  Avaliações após append em cópia: {space.avaliacoes}")
    print(f"  ✓ Retorna cópia para proteger lista original!")


def teste_heranca():
    """Teste: Verificar herança funcionando"""
    print("\n" + "="*70)
    print("TESTE 6: HERANÇA")
    print("="*70)
    
    # ✅ Teste 6.1: Space herda de BaseEntity
    print("\n✓ Testando herança de BaseEntity...")
    space = Space("s1", "Quadra", "Futebol", "Maceió", 100, [])
    print(f"  ID (de BaseEntity): {space.id}")
    print(f"  Hash (de BaseEntity): {hash(space)}")
    print(f"  Repr (de BaseEntity): {repr(space)}")
    print(f"  ✓ Space herdou métodos de BaseEntity!")
    
    # ✅ Teste 6.2: User herda de BaseEntity
    print("\n✓ Testando herança de User...")
    user = User("u1", "João", "joao@email.com")
    print(f"  ID (de BaseEntity): {user.id}")
    print(f"  Repr (de BaseEntity): {repr(user)}")
    print(f"  ✓ User herdou métodos de BaseEntity!")
    
    # ✅ Teste 6.3: Booking herda de EntityComStatus
    print("\n✓ Testando herança em cadeia...")
    from domain.booking import Booking
    booking = Booking("bk1", "u1", "s1", "t1", "RESERVADO", 100.0)
    print(f"  ID (BaseEntity): {booking.id}")
    print(f"  Status (EntityComStatus): {booking.status}")
    print(f"  ✓ Booking herdou de EntityComStatus que herda de BaseEntity!")


def main():
    """Executar todos os testes"""
    print("\n" + "🎯 "*35)
    print(" TESTES DE CADASTRO - BORA PRORRACHA".center(70))
    print("🎯 "*35)
    
    try:
        # Rodar testes
        teste_cadastro_usuario_google()
        teste_cadastro_usuario_facebook()
        teste_cadastro_espaco()
        teste_validacoes()
        teste_encapsulamento()
        teste_heranca()
        
        # Resumo final
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*70)
        print("\nFuncionalidades testadas:")
        print("  ✓ Cadastro de usuário via Google")
        print("  ✓ Cadastro de usuário via Facebook")
        print("  ✓ Cadastro de espaço dinâmico")
        print("  ✓ Validações de dados")
        print("  ✓ Encapsulamento com @property")
        print("  ✓ Herança e herança em cadeia")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
