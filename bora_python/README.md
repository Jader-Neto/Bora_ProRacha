# Bora Pro Racha


## Instalação

1. Instale o Python 3.9 ou superior.
2. Crie e ative um ambiente virtual.
3. Instale as dependências com:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação com:

```bash
python main.py
```

5. Execute os testes com:

```bash
pytest
```

Frontend — Como rodar

Se quiser usar a interface do frontend localizada em `frontend/index.html` siga um destes métodos:

- Abrir diretamente no navegador:

	- Abra o arquivo `frontend/index.html` no seu navegador (Chrome/Firefox). Certifique-se de que a API esteja rodando em `http://127.0.0.1:5000` e que `API_BASE` em `frontend/index.html` aponte para esse endereço.

- Servir com um servidor HTTP simples (recomendado):

	- Navegue até a pasta `frontend` e rode um servidor HTTP leve (Python 3.x):

```bash
cd frontend
python -m http.server 8000
```

	- Abra `http://localhost:8000` no navegador. Isso evita problemas de CORS/arquivos locais.

Pré-requisitos para rodar o frontend

- Navegador moderno (Chrome, Firefox, Edge).
- Backend rodando em `http://127.0.0.1:5000` (ver `api/app.py`).
- Se usar o servidor estático, Python 3 instalado (para `python -m http.server`).

Observações

- O frontend é uma SPA estática em `frontend/index.html` e não precisa de build nem Node.js. Ele faz chamadas `fetch()` para a API; garanta que o `API_BASE` dentro do arquivo aponte para o servidor Flask.
- Para desenvolvimento local, ative o backend primeiro com:

```bash
python api/app.py
```




# Funcionalidades e Como Foram Implementadas

## 1. Sincronização de horários

Onde está:

* [services/sync_service.py](services/sync_service.py)
* [domain/timeslot.py](domain/timeslot.py)
* [domain/booking.py](domain/booking.py)
* [domain/space.py](domain/space.py)

Como foi implementado:
A sincronização é feita pelo `SyncService`, que percorre os espaços, os intervalos de tempo e as reservas existentes.

A reserva fica com o estado controlado por `Booking`, o espaço pode entrar em manutenção com `Space`, e o `TimeSlot` muda entre `DISPONIVEL`, `RESERVADO` e `BLOQUEADO`. Assim, o serviço mantém a disponibilidade coerente com o estado real do sistema.

Conceitos aplicados:

* Encapsulamento (cada entidade controla seu próprio estado)
* Modelagem por estados

---

## 2. Cadastro rápido

Onde está:

* `domain/user.py`

Como foi implementado:
A entidade `User` controla os dados do usuário e seu nível de completude (parcial ou completo). As validações são feitas através de propriedades (`@property` e setters).

Conceitos aplicados:

* Encapsulamento
* Abstração

---

## 3. Agendamento fácil

Onde está:

* `domain/booking.py`

Como foi implementado:
O fluxo de agendamento (selecionar horário, reservar e confirmar) é implementado através de métodos dentro da classe `Booking`, que controla as transições de estado da reserva.

Conceitos aplicados:

* Encapsulamento
* Modelagem de estados

---

## 4. Filtro dinâmico

Onde está:

* `domain/filtro.py`
* `services/filter_service.py`
* `domain/interfaces.py`

Como foi implementado:
Os filtros foram implementados como classes que seguem a interface `IFiltro`. Cada filtro possui sua própria lógica no método `aplicar()`.

O `FilterService` recebe qualquer filtro e executa sem conhecer sua implementação.

```python
filtro.aplicar(lista)
```

Conceitos aplicados:

* Polimorfismo
* Abstração
* Strategy Pattern

---

## 5. Espaços detalhados

Onde está:

* `domain/space.py`

Como foi implementado:
A classe `Space` centraliza todas as informações do espaço, como localização, preço e horários disponíveis.

Conceitos aplicados:

* Encapsulamento
* Modelagem de entidade

---

## 6. Cadastro de espaço dinâmico

Onde está:

* `domain/space.py`

Como foi implementado:
A própria entidade `Space` possui métodos responsáveis por alterar seu estado, como adicionar horários, bloquear disponibilidade e atualizar informações.

Conceitos aplicados:

* Encapsulamento
* Responsabilidade única

---

## 7. Lembrete interativo

Onde está:

* [services/reminder_service.py](services/reminder_service.py)
* [domain/notification.py](domain/notification.py)
* [domain/booking.py](domain/booking.py)

Como foi implementado:
O `ReminderService` cria uma `Notification` do tipo `REMINDER` para uma reserva e guarda os lembretes pendentes. Depois ele pode enviar, cancelar ou listar esses lembretes.

Conceitos aplicados:

* Separação de responsabilidades
* Encapsulamento
* Uso de entidades para notificação

---

## 8. Fuso horário dinâmico

Onde está:

* [services/timezone_service.py](services/timezone_service.py)
* [domain/space.py](domain/space.py)

Como foi implementado:
O `TimezoneService` valida fusos horários, ajusta o fuso de um espaço e também faz conversão simplificada entre horários. O campo `timezone` da classe `Space` guarda essa informação.

Conceitos aplicados:

* Abstração
* Validação de dados
* Organização da lógica de domínio

---

## 9. Cancelamentos

Onde está:

* `domain/booking.py`

Como foi implementado:
A classe `Booking` possui métodos que alteram o estado da reserva para cancelado, além de possíveis regras associadas (como taxa ou liberação do horário).

Conceitos aplicados:

* Encapsulamento
* Modelagem por estados

---

## 10. Confirmação de agendamento (check-in)

Onde está:

* [services/checkin_service.py](services/checkin_service.py)
* [domain/booking.py](domain/booking.py)

Como foi implementado:
O `CheckinService` gera um código QR, valida se a reserva está confirmada e então chama `Booking.realizar_checkin()`. A própria reserva controla a mudança de estado para `CHECKIN_REALIZADO`.

Conceitos aplicados:

* Máquina de estados
* Encapsulamento
* Polimorfismo de comportamento via serviço


## Herança no projeto
Herança aparece principalmente em [domain/base.py](domain/base.py), [domain/user.py](domain/user.py), [domain/space.py](domain/space.py), [domain/booking.py](domain/booking.py) e [services/base.py](services/base.py).

Como funciona:
[BaseEntity](domain/base.py) centraliza o id, a comparação entre objetos e a representação textual. [EntityComStatus](domain/base.py) estende essa base para entidades que precisam de status. Em outro ponto, [BaseService](services/base.py) concentra logger e validações reutilizáveis para todos os serviços.

Motivo de existir:
isso evita repetição, padroniza regras comuns e facilita manutenção. Se a forma de tratar id, status ou logging mudar, a alteração fica concentrada na classe base.

## Polimorfismo no projeto

Polimorfismo aparece principalmente em [domain/interfaces.py](domain/interfaces.py), [domain/filtro.py](domain/filtro.py), [domain/estrategia_calculo.py](domain/estrategia_calculo.py) e [services/filter_service.py](services/filter_service.py).

Como funciona:
as interfaces definem contratos como aplicar() e calcular(). As classes concretas implementam esses métodos de formas diferentes, mas o serviço chama sempre a mesma assinatura. Por isso [FilterService](services/filter_service.py) consegue receber qualquer filtro que implemente [IFiltro](domain/interfaces.py), e cada filtro decide sua própria lógica de execução.

Motivo de existir:
isso permite trocar regras sem alterar o serviço principal. O sistema fica mais flexível para adicionar novos filtros, novas estratégias de cálculo ou novos comportamentos de notificação sem reescrever as partes já prontas.

## Arquivos principais

- [domain/base.py](domain/base.py)
- [domain/interfaces.py](domain/interfaces.py)
- [domain/filtro.py](domain/filtro.py)
- [domain/estrategia_calculo.py](domain/estrategia_calculo.py)
- [domain/user.py](domain/user.py)
- [domain/booking.py](domain/booking.py)
- [domain/space.py](domain/space.py)
- [services/base.py](services/base.py)
- [services/filter_service.py](services/filter_service.py)


---

## Padrões Aplicados

| Padrão | Categoria | Arquivos Criados | Arquivos Modificados |
|--------|-----------|------------------|----------------------|
| Builder | Criacional | `domain/space_builder.py` | `mock/mock_data.py`, `services/dynamic_space_registration_service.py`, `api/app.py` |
| State | Comportamental | `domain/states/booking_states.py`, `domain/states/notification_states.py`, `domain/states/__init__.py` | `domain/booking.py`, `domain/notification.py` |
| Facade | Estrutural | `services/booking_facade.py` | `api/app.py` |

---

## Builder

### O que é

O Builder é um padrão criacional que permite a construção de objetos complexos passo a passo, através de uma interface fluente. Em vez de passar todos os parâmetros de uma vez para o construtor, cada atributo é adicionado por um método próprio e a instância só é criada quando todos os dados estiverem prontos, através do método `.build()`.

### Por que foi escolhido

A classe `Space` é a entidade com mais atributos do projeto. Antes do Builder, toda criação de um espaço era feita diretamente no construtor com 8 parâmetros posicionais, sem nenhuma indicação de o que cada valor representava:

```python
# Antes — o que significa cada argumento?
Space("s1", "Arena Pajuçara", "Futebol", "Pajuçara, Maceió - AL", 120,
      ["https://example.com/foto1.jpg"], "DISPONIVEL", "America/Sao_Paulo")
```

Esse formato apresentava três problemas concretos:

**Argumentos posicionais sem semântica.** Com 8 parâmetros posicionais, não era possível saber o que cada valor representava sem consultar a assinatura da classe. Qualquer pessoa lendo o código precisaria abrir `space.py` para entender o que estava sendo passado em cada posição.

**Ausência de validação antes da criação.** O objeto era instanciado independentemente de ter todos os dados obrigatórios preenchidos corretamente. Se o `esporte` viesse vazio ou o `preco_hora` fosse negativo, o erro só aparecia depois, em tempo de uso — não em tempo de criação.

**Construção em etapas não era possível.** O `DynamicSpaceRegistrationService` recebe dados campo a campo de uma requisição HTTP. Com o construtor direto, era necessário ter todos os valores disponíveis ao mesmo tempo. O Builder resolve isso naturalmente: cada chamada encadeada adiciona um atributo, e o objeto só é construído quando tudo estiver pronto.

### O que mudou

```python
# Depois — cada campo é explícito e autoexplicativo
SpaceBuilder("s1", "Arena Pajuçara")
    .com_esporte("Futebol")
    .com_localizacao("Pajuçara, Maceió - AL")
    .com_preco(120)
    .com_fotos(["https://example.com/foto1.jpg"])
    .com_status("DISPONIVEL")
    .com_timezone("America/Sao_Paulo")
    .build()
```

O `.build()` passou a ser o portão de entrada: nenhum objeto `Space` é criado sem antes validar os campos obrigatórios e as regras de negócio.

---

## Facade

### O que é

O Facade é um padrão estrutural que cria uma interface simplificada para um conjunto de subsistemas complexos. O código cliente não precisa conhecer nem se comunicar diretamente com vários componentes internos — ele fala com a Facade, e ela resolve o restante. O nome vem da arquitetura: a fachada de um prédio é tudo que você vê, independente de toda a estrutura interna.

### Por que foi escolhido

O `app.py` acumulava duas responsabilidades distintas ao mesmo tempo: ser uma camada HTTP e ser um orquestrador de negócio. Cada rota coordenava manualmente a sequência de operações entre múltiplos serviços internos:

```python
# Antes — 30+ linhas de lógica de negócio dentro de uma rota HTTP
@app.post('/api/reservations')
def create_reservation():
    data = request.get_json() or {}
    # ... extração de parâmetros ...

    agora = datetime.now()
    inicio = agora + timedelta(hours=1)
    fim = inicio + timedelta(hours=2)

    slot = TimeSlot(slot_id=gen_id('ts'), space_id=space_id,
                    inicio=inicio, fim=fim, status='DISPONIVEL')

    reserva = booking_service.criar_reserva_rapida(
        user_id=user_id, space_id=space_id,
        slot_id=slot.id, valor_total=float(valor)
    )
    reserva.confirmar()

    pagamento = {
        'id': gen_id('p'), 'reservaId': reserva.id,
        'metodo': data.get('metodo', 'Cartão de Crédito'),
        'ultimos4': data.get('ultimos4', '0000'),
        'valor': valor, 'data': datetime.now().strftime('%d/%m/%Y'),
        'status': 'Aprovado'
    }

    return jsonify({'reserva': {...}, 'pagamento': pagamento}), 201
```

O mesmo padrão se repetia nas rotas de checkin, cancelamento e lembrete — cada uma instanciava serviços, coordenava operações e montava respostas diretamente no controlador HTTP. Isso gerava três consequências diretas:

**Lógica de negócio na camada HTTP.** A rota sabia que era preciso criar um `TimeSlot` antes do `Booking`. Sabia que após criar o booking era necessário chamar `confirmar()`. Sabia como montar o objeto de pagamento. Nenhum desses detalhes deveria estar numa rota HTTP.

**Acoplamento total entre rotas e serviços.** O `app.py` importava e instanciava `EasyBookingService`, `CheckinService`, `CancellationService` e `ReminderService` diretamente. A camada HTTP conhecia toda a estrutura interna de serviços.

**Impossibilidade de reutilizar o fluxo.** Qualquer novo ponto de entrada da aplicação — uma CLI, testes de integração, outro endpoint — precisaria replicar toda a sequência de operações manualmente.

### O que mudou

A `BookingFacade` centralizou os fluxos completos de negócio. Os serviços internos continuam existindo exatamente como eram — o que mudou foi a criação de uma camada de orquestração entre eles e qualquer cliente externo:

```python
# services/booking_facade.py

class BookingFacade:
    def __init__(self, ...):
        self._booking_svc = EasyBookingService()
        self._checkin_svc = CheckinService()
        self._cancellation_svc = CancellationService()
        self._reminder_svc = ReminderService()

    def reservar(self, user_id, space_id, valor, local, horario, ...):
        slot = TimeSlot(slot_id=_gen_id("ts"), ...)
        booking = self._booking_svc.criar_reserva_rapida(...)
        booking.confirmar()
        self._reminder_svc.agendar_lembrete(booking, horas_lembrete)
        return {"reserva": {...}, "pagamento": {...}}

    def fazer_checkin(self, booking_id, user_id):
        booking = Booking(booking_id, ..., status="CONFIRMADO")
        qr_code = self._checkin_svc.gerar_codigo_qr(booking)
        checkin_info = self._checkin_svc.realizar_checkin(booking)
        return {"reserva_id": booking_id, "qr_code": qr_code, ...}

    def cancelar(self, booking_id, tempo_antecedencia_horas, ...):
        booking = Booking(booking_id, ..., valor_total=valor_total)
        return self._cancellation_svc.cancelar_com_politica(booking, ...)

    def agendar_lembrete(self, booking_id, user_id, horas_antes):
        booking = Booking(booking_id, user_id, ...)
        notificacao = self._reminder_svc.agendar_lembrete(booking, horas_antes)
        return {"id": notificacao.id, "titulo": notificacao.titulo, ...}
```

As rotas do `app.py` passaram a ter uma única responsabilidade — receber a requisição e delegar:

```python
# Depois — 5 linhas por rota, sem lógica de negócio
@app.post('/api/reservations')
def create_reservation():
    data = request.get_json() or {}
    if not data.get('user_id') or not data.get('space_id'):
        return jsonify({"error": "user_id e space_id são obrigatórios"}), 400
    resultado = booking_facade.reservar(user_id=data['user_id'],
                                        space_id=data['space_id'],
                                        valor=data.get('valor', 0), ...)
    return jsonify(resultado), 201

@app.post('/api/reservations/<res_id>/checkin')
def do_checkin(res_id):
    return jsonify(booking_facade.fazer_checkin(res_id))

@app.post('/api/reservations/<res_id>/cancel')
def cancel_reservation(res_id):
    data = request.get_json() or {}
    return jsonify(booking_facade.cancelar(
        booking_id=res_id,
        tempo_antecedencia_horas=data.get('tempo_antecedencia_horas', 24),
    ))
```

Os imports de `EasyBookingService`, `CheckinService`, `CancellationService` e `ReminderService` foram completamente removidos do `app.py`. A camada HTTP agora conhece apenas a `BookingFacade`.

### Por que foi a melhor opção estrutural

O Facade atacou o problema de maior impacto arquitetural do projeto: o vazamento de lógica de negócio para a camada HTTP. Enquanto o Builder resolvia um problema localizado na criação de `Space` e o Proxy adicionaria uma camada de cache sobre o repositório, o Facade reorganizou como as camadas inteiras do sistema se comunicam. Qualquer melhoria feita nos serviços internos agora beneficia automaticamente todas as rotas, porque o ponto de contato é único. E qualquer novo cliente que precise acionar o fluxo de reserva encontra uma interface clara e completa, sem precisar entender como os quatro serviços internos se relacionam.

---

## State

### O que é

O State é um padrão comportamental que permite a um objeto alterar seu comportamento conforme seu estado interno muda. Em vez de acumular condicionais dentro da classe para tratar cada situação, cada estado vira uma classe separada com suas próprias regras. O objeto simplesmente delega as ações para o estado atual, que sabe exatamente o que é permitido ou não a partir dele.

### Por que foi escolhido

Tanto `Booking` quanto `Notification` são entidades com ciclos de vida bem definidos. O `Booking` possui 6 estados (`RESERVADO`, `CONFIRMADO`, `CHECKIN_REALIZADO`, `CANCELADO`, `NAO_COMPARECEU`, `REEMBOLSADO`) e a `Notification` possui 4 (`PENDENTE`, `ENVIADA`, `LIDA`, `FALHA`). Cada uma dessas entidades é, na essência, uma máquina de estados — mas essa máquina estava implementada de forma implícita, espalhada dentro dos próprios métodos como blocos `if/elif`:

```python
# Antes — cada método conhecia todos os estados possíveis
def confirmar(self) -> None:
    if self.status != "RESERVADO":
        raise ValueError("Apenas reservas podem ser confirmadas")
    self.status = "CONFIRMADO"

def cancelar(self, taxa: float = 0.0) -> None:
    if self.status in ["CANCELADO", "NAO_COMPARECEU"]:
        raise ValueError(f"Não pode cancelar reserva com status {self.status}")
    self._taxa_cancelamento = taxa
    self.status = "CANCELADO"

def realizar_checkin(self) -> None:
    if self.status != "CONFIRMADO":
        raise ValueError("Apenas reservas confirmadas podem fazer check-in")
    self.status = "CHECKIN_REALIZADO"
```

Essa abordagem gerava três problemas concretos:

**Cada método conhecia todos os estados possíveis.** Para decidir se `confirmar()` era permitido, o método precisava saber que existia o estado `RESERVADO` e que qualquer outro deveria ser rejeitado. Esse conhecimento estava duplicado entre todos os métodos. Com 5 métodos de transição e 6 estados, a complexidade era de 30 combinações espalhadas pelo código. Adicionar um novo estado obrigava a revisar todos os métodos da classe.

**Regras de transição inconsistentes.** O código original permitia cancelar uma reserva após o check-in ser realizado, pois `cancelar()` só bloqueava `CANCELADO` e `NAO_COMPARECEU`, sem considerar `CHECKIN_REALIZADO`. Essa inconsistência existia porque as regras estavam fragmentadas entre os métodos, sem uma visão unificada do que cada estado permitia ou proibia.

**Impossibilidade de reconstituir o estado correto.** Quando um `Booking` era criado com um `status` vindo do banco de dados, como `status="CONFIRMADO"`, o objeto não tinha como traduzir isso em comportamento — era apenas uma string. O estado não era um cidadão de primeira classe no domínio.

### O que mudou

Cada estado do ciclo de vida virou uma classe própria dentro de `domain/states/`. O `Booking` e a `Notification` deixaram de ser guardiões das regras de transição e passaram a ser apenas detentores do estado atual, delegando todas as decisões:

```python
# domain/states/booking_states.py

class EstadoReservado(EstadoBooking):
    nome = "RESERVADO"

    def confirmar(self, booking):
        booking._set_estado(EstadoConfirmado())     # permitido

    def cancelar(self, booking, taxa):
        booking._taxa_cancelamento = taxa
        booking._set_estado(EstadoCancelado())      # permitido

    def realizar_checkin(self, booking):
        raise ValueError("Confirme a reserva antes de realizar o check-in")

    def marcar_nao_comparecimento(self, booking):
        raise ValueError("Reserva ainda não foi confirmada")

    def reembolsar(self, booking):
        raise ValueError("Apenas reservas canceladas podem ser reembolsadas")


class EstadoCheckinRealizado(EstadoBooking):
    nome = "CHECKIN_REALIZADO"

    def cancelar(self, booking, taxa):
        raise ValueError("Não é possível cancelar após o check-in")  # inconsistência corrigida
    # ...
```

O `Booking` passou a ter métodos de uma única linha:

```python
# domain/booking.py

class Booking(EntityComStatus):
    def __init__(self, ..., status="RESERVADO"):
        # Estado inicializado a partir do status recebido — resolve a reconstituição do banco
        self._estado = ESTADOS_BOOKING.get(status, EstadoReservado())

    def _set_estado(self, novo_estado):
        self._estado = novo_estado
        self.status = novo_estado.nome

    def confirmar(self):
        self._estado.confirmar(self)

    def cancelar(self, taxa=0.0):
        self._estado.cancelar(self, taxa)

    def realizar_checkin(self):
        self._estado.realizar_checkin(self)

    def marcar_nao_comparecimento(self):
        self._estado.marcar_nao_comparecimento(self)

    def reembolsar(self):
        self._estado.reembolsar(self)
```

O mesmo foi aplicado na `Notification`. O estado `FALHA` ganhou também uma regra de reenvio — uma notificação que falhou pode chamar `marcar_enviada()` e voltar ao estado `ENVIADA`, comportamento que não existia antes e que seria difícil de adicionar sem o State:

```python
class EstadoFalha(EstadoNotification):
    nome = "FALHA"

    def marcar_enviada(self, notification):
        # Reenvio após falha — regra nova adicionada sem alterar Notification
        notification.data_envio = datetime.now()
        notification._set_estado(EstadoEnviada())
```

O dicionário `ESTADOS_BOOKING` resolve o problema de reconstituição a partir do banco de dados: quando um `Booking` é criado com `status="CONFIRMADO"`, o construtor já inicializa o objeto com o comportamento correto de um booking confirmado, não apenas com uma string que representa isso.

### Estrutura de arquivos criada

```
domain/
  states/
    __init__.py                  ← exporta todos os estados
    booking_states.py            ← 6 classes + ESTADOS_BOOKING
    notification_states.py       ← 4 classes + ESTADOS_NOTIFICATION
  booking.py                     ← refatorado para delegar ao estado
  notification.py                ← refatorado para delegar ao estado
```

### Por que foi a melhor opção comportamental

O Observer seria o segundo lugar, pois faz sentido para disparar notificações automáticas quando o `Booking` muda de estado. Mas o Observer resolve um problema de comunicação entre camadas, enquanto o State resolve um problema estrutural dentro das entidades mais centrais do sistema. Mais do que isso: o Observer se beneficia diretamente do State. Com estados bem definidos e isolados, adicionar um Observer é trivial — o método `_set_estado()` é o ponto natural para disparar eventos. Implementar Observer sem State significaria ainda ter `if/elif` dentro do `Booking` antes de notificar os observadores.

