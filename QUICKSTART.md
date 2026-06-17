"""
GUIA DE INÍCIO RÁPIDO
BORA PRORRACHA - Python Implementation
"""

# ============================================================================
# 1. INSTALAÇÃO
# ============================================================================

# Abra o terminal (PowerShell, CMD ou Git Bash)
# Navegue até o diretório do projeto

cd bora_python

# Instale as dependências
pip install -r requirements.txt


# ============================================================================
# 2. EXECUTAR A APLICAÇÃO COMPLETA
# ============================================================================

# Demonstra todas as 10 funcionalidades
python main.py


# ============================================================================
# 3. EXECUTAR OS TESTES
# ============================================================================

# Todos os testes
pytest

# Com verbosidade (mais detalhes)
pytest -v

# Com cobertura
pytest --cov=domain --cov=services

# Gerar relatório HTML
pytest --cov=domain --cov=services --cov-report=html
# Abra: htmlcov/index.html no navegador


# ============================================================================
# 4. EXEMPLOS DE USO NO CÓDIGO
# ============================================================================

# Exemplo 1: Usar FilterService
from services.filter_service import FilterService
from mock.mock_data import mock_spaces

filter_service = FilterService()
spaces_maceio = filter_service.filtrar_por_local(mock_spaces, "Maceió")
print(f"Espaços em Maceió: {len(spaces_maceio)}")


# Exemplo 2: Criar e confirmar uma reserva
from services.easy_booking_service import EasyBookingService
from mock.mock_data import mock_slots

easy_booking = EasyBookingService()

# Selecionar horário
slot = [s for s in mock_slots if s.status == "DISPONIVEL"][0]
easy_booking.selecionar_horario(slot)

# Criar reserva
reserva = easy_booking.criar_reserva_rapida("u1", "s1", slot.id, 120.0)
print(f"Reserva criada: {reserva.id}")

# Confirmar
reserva_confirmada = easy_booking.confirmar_reserva(reserva)
print(f"Status: {reserva_confirmada.status}")


# Exemplo 3: Avaliar espaço
from services.detailed_space_service import DetailedSpaceService

detailed = DetailedSpaceService()
detailed.adicionar_avaliacao("s1", 5)
detailed.adicionar_avaliacao("s1", 4)
media = detailed.obter_media_avaliacoes("s1")
print(f"Avaliação média: {media}/5 ⭐")


# Exemplo 4: Filtro avançado
spaces_filtrados = filter_service.filtrar_avancado(
    mock_spaces,
    local="Maceió",
    esporte="Futebol",
    preco_maximo=150
)


# Exemplo 5: Cancelar com política
from services.cancellation_service import CancellationService
from mock.mock_data import mock_bookings

cancellation = CancellationService()
booking = mock_bookings[0]

# Cancelar com antecedência de 25 horas (sem taxa)
resultado = cancellation.cancelar_com_politica(booking, 25)
print(f"Reembolso: R$ {resultado['reembolso']:.2f}")


# ============================================================================
# 5. ESTRUTURA DO PROJETO
# ============================================================================

"""
bora_python/
├── domain/                    # Entidades e Interfaces
│   ├── base.py               # Classes base
│   ├── interfaces.py         # Interfaces ABC
│   ├── user.py               # Usuário
│   ├── space.py              # Espaço esportivo
│   ├── booking.py            # Reserva
│   ├── timeslot.py           # Horário
│   ├── notification.py       # Notificação
│   ├── filtro.py             # Estratégias de filtro
│   └── estrategia_calculo.py # Estratégias de cálculo
│
├── services/                 # Lógica de Negócio (10 serviços)
│   ├── base.py               # BaseService
│   ├── base_repository.py    # Repository genérico
│   ├── sync_service.py              # Sincronização
│   ├── quick_registration_service.py # Cadastro Rápido
│   ├── easy_booking_service.py       # Agendamento Fácil
│   ├── filter_service.py             # Filtros
│   ├── detailed_space_service.py     # Espaços Detalhados
│   ├── dynamic_space_registration_service.py # Cadastro Dinâmico
│   ├── reminder_service.py           # Lembretes
│   ├── timezone_service.py           # Timezones
│   ├── cancellation_service.py       # Cancelamentos
│   └── checkin_service.py            # Check-in
│
├── mock/                     # Dados de Teste
│   └── mock_data.py          # 20+ objetos mockados
│
├── tests/                    # Testes (60+)
│   ├── test_domain.py        # Testes de entidades
│   ├── test_services.py      # Testes de serviços
│   └── conftest.py           # Configuração pytest
│
├── main.py                   # Aplicação principal
├── README.md                 # Documentação completa
├── requirements.txt          # Dependências
├── setup.py                  # Configuração
└── pytest.ini                # Config pytest
"""


# ============================================================================
# 6. FUNCIONALIDADES
# ============================================================================

"""
1. SINCRONIZAÇÃO - Sincroniza estado de espaços com time slots
2. CADASTRO RÁPIDO - Login com Google/Facebook
3. AGENDAMENTO FÁCIL - Criar reservas rapidamente
4. FILTRO DINÂMICO - Filtrar espaços por vários critérios
5. ESPAÇOS DETALHADOS - Informações completas + avaliações
6. CADASTRO DINÂMICO - Registrar novos espaços
7. LEMBRETES - Agendamento de notificações
8. TIMEZONES - Gerenciar timezones diferentes
9. CANCELAMENTOS - Políticas de cancelamento
10. CHECK-IN - QR code e confirmação de check-in
"""


# ============================================================================
# 7. PADRÕES DE DESIGN
# ============================================================================

"""
✓ Strategy Pattern - Diferentes estratégias de filtro e cálculo
✓ Composite Pattern - Combinar múltiplos filtros
✓ Repository Pattern - CRUD genérico
✓ Factory Pattern - Geração de IDs
✓ Encapsulation - Atributos privados com @property
✓ Inheritance & Polymorphism - Hierarquia de classes
"""


# ============================================================================
# 8. TÉCNICAS PYTHON
# ============================================================================

"""
✓ Type Hints - Anotações de tipo
✓ ABC - Abstract Base Classes
✓ Properties - @property, @setter
✓ Decorators - @abstractmethod
✓ Generics - TypeVar, Generic
✓ List Comprehensions - Filtragem elegante
✓ F-strings - Formatação moderna
✓ Logging - Sistema de logs
✓ Exception Handling - Tratamento robusto
"""


# ============================================================================
# 9. TROUBLESHOOTING
# ============================================================================

# Erro: "ModuleNotFoundError: No module named 'domain'"
# Solução: Execute do diretório bora_python
cd bora_python
python main.py

# Erro: "No module named pytest"
# Solução: Instale as dependências
pip install -r requirements.txt

# Erro: "Python command not found"
# Solução: Use python3 no Linux/Mac, ou adicione Python ao PATH no Windows


# ============================================================================
# 10. PRÓXIMOS PASSOS
# ============================================================================

# 1. Explore o código em domain/ e services/
# 2. Execute os testes para ver a cobertura
# 3. Modifique mock_data.py para adicionar mais dados
# 4. Adicione seus próprios serviços
# 5. Crie um cliente HTTP (FastAPI) para consumir os serviços
# 6. Integre com banco de dados (SQLAlchemy)


# ============================================================================
# 11. RECURSOS
# ============================================================================

# Documentação Principal:
# - README.md - Guia completo
# - RESUMO_IMPLEMENTACAO.md - Resumo técnico

# Código Exemplo:
# - main.py - Demonstra todas as 10 features

# Testes:
# - tests/test_domain.py - 25+ testes
# - tests/test_services.py - 35+ testes


print("""
╔════════════════════════════════════════════════════════════════╗
║   BORA PRORRACHA - Python Implementation - v1.0               ║
║   ✓ 10 Funcionalidades                                        ║
║   ✓ 60+ Testes                                                ║
║   ✓ Código Profissional                                       ║
║   ✓ Documentação Completa                                     ║
║                                                                ║
║   Comando para começar:                                       ║
║   python main.py                                              ║
╚════════════════════════════════════════════════════════════════╝
""")
