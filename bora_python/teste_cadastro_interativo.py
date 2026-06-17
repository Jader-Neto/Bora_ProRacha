#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Interativo de Teste de Cadastro
Permite testar com seus próprios dados
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from domain.user import User
from domain.space import Space
from services.quick_registration_service import QuickRegistrationService
from services.dynamic_space_registration_service import DynamicSpaceRegistrationService


def menu():
    print("\n" + "="*60)
    print("🎯 TESTE INTERATIVO DE CADASTRO - BORA PRO RACHA".center(60))
    print("="*60)
    print("\nEscolha uma opção:")
    print("1. Cadastrar usuário via Google")
    print("2. Cadastrar usuário via Facebook")
    print("3. Cadastrar espaço")
    print("4. Testar validação de email")
    print("5. Testar validação de preço")
    print("6. Ver exemplo completo")
    print("0. Sair")
    
    opcao = input("\nDigite a opção (0-6): ").strip()
    return opcao


def cadastro_google():
    print("\n--- CADASTRO VIA GOOGLE ---")
    email = input("Email (ex: joao@gmail.com): ").strip()
    
    if not email or "@" not in email:
        print("❌ Email inválido!")
        return
    
    service = QuickRegistrationService()
    usuario = service.login_com_google(email)
    
    print(f"\n✅ Usuário criado!")
    print(f"  ID: {usuario.id}")
    print(f"  Nome: {usuario.nome}")
    print(f"  Email: {usuario.email}")
    print(f"  Status: {usuario.status}")
    print(f"  Progresso: {service.obter_progresso_cadastro(usuario)}%")
    
    completar = input("\nDeseja completar o cadastro? (s/n): ").lower()
    if completar == 's':
        telefone = input("Digite o telefone: ").strip()
        try:
            usuario.completar_cadastro(telefone)
            print(f"\n✅ Cadastro completado!")
            print(f"  Status: {usuario.status}")
            print(f"  Telefone: {usuario.telefone}")
            print(f"  Progresso: {service.obter_progresso_cadastro(usuario)}%")
            print(f"  Pode fazer reservas? {usuario.pode_reservar()}")
        except ValueError as e:
            print(f"❌ Erro: {e}")


def cadastro_facebook():
    print("\n--- CADASTRO VIA FACEBOOK ---")
    email = input("Email (ex: maria@facebook.com): ").strip()
    nome = input("Nome completo: ").strip()
    
    if not email or "@" not in email:
        print("❌ Email inválido!")
        return
    
    if not nome:
        print("❌ Nome não pode ser vazio!")
        return
    
    service = QuickRegistrationService()
    usuario = service.login_com_facebook(email, nome)
    
    print(f"\n✅ Usuário criado!")
    print(f"  ID: {usuario.id}")
    print(f"  Nome: {usuario.nome}")
    print(f"  Email: {usuario.email}")
    print(f"  Status: {usuario.status}")
    print(f"  Progresso: {service.obter_progresso_cadastro(usuario)}%")


def cadastro_espaco():
    print("\n--- CADASTRO DE ESPAÇO ---")
    nome = input("Nome do espaço (ex: Quadra Nova): ").strip()
    esporte = input("Esporte (ex: Futebol): ").strip()
    localizacao = input("Localização (ex: Maceió): ").strip()
    
    try:
        preco = float(input("Preço por hora (ex: 85.00): "))
    except ValueError:
        print("❌ Preço deve ser um número!")
        return
    
    fotos_str = input("Fotos (separadas por vírgula ou Enter para pular): ").strip()
    fotos = [f.strip() for f in fotos_str.split(",")] if fotos_str else []
    
    service = DynamicSpaceRegistrationService()
    
    try:
        espaco = service.cadastrar_espaco(
            nome=nome,
            esporte=esporte,
            localizacao=localizacao,
            preco_hora=preco,
            timezone="America/Sao_Paulo",
            fotos=fotos
        )
        
        print(f"\n✅ Espaço cadastrado!")
        print(f"  ID: {espaco.id}")
        print(f"  Nome: {espaco.nome}")
        print(f"  Esporte: {espaco.esporte}")
        print(f"  Localização: {espaco.localizacao}")
        print(f"  Preço/hora: R$ {espaco.preco_hora}")
        print(f"  Status: {espaco.status}")
        print(f"  Fotos: {len(espaco.fotos)}")
        
    except ValueError as e:
        print(f"❌ Erro: {e}")


def validar_email():
    print("\n--- TESTE DE EMAIL ---")
    email = input("Digite um email para validar: ").strip()
    
    try:
        user = User("u_test", "Teste", email)
        print(f"✅ Email válido! {email}")
    except ValueError as e:
        print(f"❌ Email inválido! {e}")


def validar_preco():
    print("\n--- TESTE DE PREÇO ---")
    try:
        preco = float(input("Digite um preço para validar: "))
        space = Space("s_test", "Teste", "Teste", "Teste", preco, [])
        print(f"✅ Preço válido! R$ {preco}")
    except ValueError as e:
        print(f"❌ Preço inválido! {e}")


def exemplo_completo():
    print("\n--- EXEMPLO COMPLETO ---")
    print("\n1️⃣ Criando usuário...")
    service = QuickRegistrationService()
    usuario = service.login_com_google("demo@gmail.com")
    usuario.completar_cadastro("85987654321")
    print(f"   ✓ {usuario.nome} cadastrado!")
    
    print("\n2️⃣ Registrando espaço...")
    service_space = DynamicSpaceRegistrationService()
    espaco = service_space.cadastrar_espaco(
        "Quadra Demo",
        "Futebol",
        "Maceió",
        100.0,
        "America/Sao_Paulo",
        ["foto1.jpg"]
    )
    print(f"   ✓ {espaco.nome} registrado!")
    
    print("\n3️⃣ Verificando dados...")
    print(f"   Usuário: {usuario.nome} (Status: {usuario.status})")
    print(f"   Espaço: {espaco.nome} (R$ {espaco.preco_hora}/h)")
    print(f"   ✓ Usuário pode fazer reservas? {usuario.pode_reservar()}")
    print(f"   ✓ Espaço está disponível? {service_space.verificar_disponibilidade(espaco.id)}")
    
    print("\n✅ Exemplo completado com sucesso!")


def main():
    while True:
        opcao = menu()
        
        if opcao == "1":
            cadastro_google()
        elif opcao == "2":
            cadastro_facebook()
        elif opcao == "3":
            cadastro_espaco()
        elif opcao == "4":
            validar_email()
        elif opcao == "5":
            validar_preco()
        elif opcao == "6":
            exemplo_completo()
        elif opcao == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
