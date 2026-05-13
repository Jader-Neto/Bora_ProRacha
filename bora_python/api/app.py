from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.user import User
from domain.space import Space
from domain.space_builder import SpaceBuilder
from domain.booking import Booking
from domain.timeslot import TimeSlot
from services.quick_registration_service import QuickRegistrationService
from services.dynamic_space_registration_service import DynamicSpaceRegistrationService
from services.easy_booking_service import EasyBookingService
from services.filter_service import FilterService
from services.checkin_service import CheckinService
from services.cancellation_service import CancellationService
from services.reminder_service import ReminderService

SPACE_STATUS_AVAILABLE = "Disponível"

app = Flask(__name__)
CORS(app)

quick_reg_service = QuickRegistrationService()
space_service = DynamicSpaceRegistrationService()
booking_service = EasyBookingService()
filter_service = FilterService()
checkin_service = CheckinService()
cancellation_service = CancellationService()
reminder_service = ReminderService()

SPACES = [
    {
        "nome": "Arena Futsal Central",
        "tipo": "Esporte",
        "modalidade": "Futsal",
        "inicio": "18:00",
        "fim": "20:00",
        "local": "Pajuçara, Maceió - AL, Av. Dr. Antônio Gouveia, 150",
        "status": SPACE_STATUS_AVAILABLE
    },
    {
        "nome": "Campo do Parque",
        "tipo": "Esporte",
        "modalidade": "Futebol",
        "inicio": "19:00",
        "fim": "21:00",
        "local": "Jatiúca, Maceió - AL, Rua Carlos Jundiaí, 45",
        "status": SPACE_STATUS_AVAILABLE
    },
    {
        "nome": "Quadra Olímpica",
        "tipo": "Esporte",
        "modalidade": "Basquete",
        "inicio": "18:30",
        "fim": "20:30",
        "local": "Farol, Maceió - AL, Rua Santa Luzia, 220",
        "status": SPACE_STATUS_AVAILABLE
    }
]

USERS = {}  # user_id -> user dict
RESERVATIONS = []


def gen_id(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


@app.get('/api/quadras')
def get_quadras():
    return jsonify(SPACES)


@app.post('/api/login')
def login():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "email obrigatório"}), 400

        usuario = quick_reg_service.login_com_google(email)
        
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'telefone': usuario.telefone or '',
            'status': usuario.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post('/api/signup')
def signup():
    try:
        data = request.get_json() or {}
        nome = data.get('nome')
        email = data.get('email')
        telefone = data.get('telefone', '')
        
        if not nome or not email:
            return jsonify({"error": "nome e email são obrigatórios"}), 400

        usuario = quick_reg_service.login_com_google(email)
        usuario.nome = nome
        if telefone:
            usuario.completar_cadastro(telefone)
        
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'telefone': usuario.telefone or '',
            'status': usuario.status
        }), 201
    except ValueError as e:
        print(f"[SIGNUP] ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"[SIGNUP] Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500


@app.post('/api/reservations')
def create_reservation():
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        space_id = data.get('space_id')
        local = data.get('local')
        horario = data.get('horario')
        valor = data.get('valor', 0)
        
        if not user_id or not space_id:
            return jsonify({"error": "user_id e space_id são obrigatórios"}), 400

        agora = datetime.now()
        inicio = agora + timedelta(hours=1)
        fim = inicio + timedelta(hours=2)
        
        slot = TimeSlot(
            slot_id=gen_id('ts'),
            space_id=space_id,
            inicio=inicio,
            fim=fim,
            status='DISPONIVEL'
        )
        
        reserva = booking_service.criar_reserva_rapida(
            user_id=user_id,
            space_id=space_id,
            slot_id=slot.id,
            valor_total=float(valor) if valor else 0.0
        )
        
        reserva.confirmar()
        
        pagamento = {
            'id': gen_id('p'),
            'reservaId': reserva.id,
            'metodo': data.get('metodo', 'Cartão de Crédito'),
            'ultimos4': data.get('ultimos4', '0000'),
            'valor': valor,
            'data': datetime.now().strftime('%d/%m/%Y'),
            'status': 'Aprovado'
        }

        return jsonify({
            'reserva': {
                'id': reserva.id,
                'user_id': reserva.user_id,
                'space_id': reserva.space_id,
                'local': local,
                'horario': horario,
                'status': reserva.status,
                'data': datetime.now().strftime('%d/%m/%Y'),
                'valor': str(valor)
            },
            'pagamento': pagamento
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get('/api/users/<user_id>/reservations')
def list_user_reservations(user_id):
    user_res = [r for r in RESERVATIONS if r.get('user_id') == user_id]
    return jsonify(user_res)


@app.post('/api/reservations/<res_id>/checkin')
def do_checkin(res_id):
    try:
        booking = Booking(
            booking_id=res_id,
            user_id='demo_user',
            space_id='demo_space',
            slot_id='demo_slot',
            status='CONFIRMADO'
        )
        
        qr_code = checkin_service.gerar_codigo_qr(booking)
        
        checkin_info = checkin_service.realizar_checkin(booking)
        
        return jsonify({
            'reserva_id': res_id,
            'qr_code': qr_code,
            'checkin': checkin_info,
            'status': 'CHECKIN_REALIZADO'
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post('/api/reservations/<res_id>/cancel')
def cancel_reservation(res_id):
    try:
        data = request.get_json() or {}
        tempo_antecedencia = data.get('tempo_antecedencia_horas', 24)
        
        booking = Booking(
            booking_id=res_id,
            user_id='demo_user',
            space_id='demo_space',
            slot_id='demo_slot',
            status='CONFIRMADO',
            valor_total=100.0
        )
        
        resultado = cancellation_service.cancelar_com_politica(
            booking,
            tempo_antecedencia
        )
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post('/api/reservations/<res_id>/reminder')
def create_reminder(res_id):
    try:
        data = request.get_json() or {}
        horas_antes = data.get('horas_antes', 24)
        
        booking = Booking(
            booking_id=res_id,
            user_id=data.get('user_id', 'demo_user'),
            space_id='demo_space',
            slot_id='demo_slot',
            status='CONFIRMADO'
        )
        
        notificacao = reminder_service.agendar_lembrete(booking, horas_antes)
        
        return jsonify({
            'id': notificacao.id,
            'user_id': notificacao.user_id,
            'titulo': notificacao.titulo,
            'mensagem': notificacao.mensagem,
            'status': notificacao.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get('/api/quadras/filtro')
def filter_quadras():
    try:
        local = request.args.get('local')
        esporte = request.args.get('esporte')
        preco_maximo = request.args.get('preco_maximo', type=float)
        
        spaces = []
        for s in SPACES:
            space = (SpaceBuilder(s.get('id', gen_id('s')), s['nome'])
                .com_esporte(s.get('modalidade', 'Geral'))
                .com_localizacao(s.get('local', 'Maceió'))
                .com_preco(100.0)
                .com_status('DISPONIVEL')
                .build())
            spaces.append(space)
        
        resultado = filter_service.filtrar_avancado(
            spaces,
            local=local,
            esporte=esporte,
            preco_maximo=preco_maximo
        )
        
        return jsonify([{
            'nome': s.nome,
            'esporte': s.esporte,
            'localizacao': s.localizacao,
            'preco_hora': s.preco_hora,
            'status': s.status
        } for s in resultado])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
