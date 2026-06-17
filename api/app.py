"""
app.py — Camada HTTP

Padrão Facade aplicado: cada rota delega para BookingFacade em vez de
orquestrar múltiplos serviços diretamente. As rotas passaram de blocos
de 15-25 linhas para 3-5 linhas, sem lógica de negócio na camada HTTP.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.space_builder import SpaceBuilder
from services.quick_registration_service import QuickRegistrationService
from services.dynamic_space_registration_service import DynamicSpaceRegistrationService
from services.filter_service import FilterService
from services.booking_facade import BookingFacade
import time

SPACE_STATUS_AVAILABLE = "Disponível"

frontend_dir = Path(__file__).parent.parent / "frontend"
app = Flask(__name__, static_folder=str(frontend_dir), static_url_path="")
CORS(app)

# Serviços que NÃO passam pela Facade (fora do domínio de reserva)
quick_reg_service = QuickRegistrationService()
space_service = DynamicSpaceRegistrationService()
filter_service = FilterService()

# Facade única para tudo relacionado a reservas
booking_facade = BookingFacade()

SPACES = [
    {
        "nome": "Arena Futsal Central",
        "tipo": "Esporte",
        "modalidade": "Futsal",
        "inicio": "18:00",
        "fim": "20:00",
        "local": "Pajuçara, Maceió - AL, Av. Dr. Antônio Gouveia, 150",
        "status": SPACE_STATUS_AVAILABLE,
    },
    {
        "nome": "Campo do Parque",
        "tipo": "Esporte",
        "modalidade": "Futebol",
        "inicio": "19:00",
        "fim": "21:00",
        "local": "Jatiúca, Maceió - AL, Rua Carlos Jundiaí, 45",
        "status": SPACE_STATUS_AVAILABLE,
    },
    {
        "nome": "Quadra Olímpica",
        "tipo": "Esporte",
        "modalidade": "Basquete",
        "inicio": "18:30",
        "fim": "20:30",
        "local": "Farol, Maceió - AL, Rua Santa Luzia, 220",
        "status": SPACE_STATUS_AVAILABLE,
    },
]

RESERVATIONS = []


def gen_id(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


# ── Rotas estáticas ────────────────────────────────────────────────────────
@app.route("/")
def index():
    from flask import send_from_directory
    return send_from_directory(str(frontend_dir), "index.html")


@app.get("/api/quadras")
def get_quadras():
    return jsonify(SPACES)


# ── Autenticação ───────────────────────────────────────────────────────────
@app.post("/api/login")
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email")
        if not email:
            return jsonify({"error": "email obrigatório"}), 400
        usuario = quick_reg_service.login_com_google(email)
        return jsonify({
            "id": usuario.id, "nome": usuario.nome,
            "email": usuario.email, "telefone": usuario.telefone or "",
            "status": usuario.status,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/signup")
def signup():
    try:
        data = request.get_json() or {}
        nome, email, telefone = data.get("nome"), data.get("email"), data.get("telefone", "")
        if not nome or not email:
            return jsonify({"error": "nome e email são obrigatórios"}), 400
        usuario = quick_reg_service.login_com_google(email)
        usuario.nome = nome
        if telefone:
            usuario.completar_cadastro(telefone)
        return jsonify({
            "id": usuario.id, "nome": usuario.nome,
            "email": usuario.email, "telefone": usuario.telefone or "",
            "status": usuario.status,
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500


# ── Reservas — todas delegadas à Facade ───────────────────────────────────
@app.post("/api/reservations")
def create_reservation():
    try:
        data = request.get_json() or {}
        user_id, space_id = data.get("user_id"), data.get("space_id")
        if not user_id or not space_id:
            return jsonify({"error": "user_id e space_id são obrigatórios"}), 400

        resultado = booking_facade.reservar(
            user_id=user_id,
            space_id=space_id,
            valor=data.get("valor", 0),
            local=data.get("local", ""),
            horario=data.get("horario", ""),
            metodo_pagamento=data.get("metodo", "Cartão de Crédito"),
            ultimos4=data.get("ultimos4", "0000"),
        )
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/users/<user_id>/reservations")
def list_user_reservations(user_id):
    return jsonify([r for r in RESERVATIONS if r.get("user_id") == user_id])


@app.post("/api/reservations/<res_id>/checkin")
def do_checkin(res_id):
    try:
        return jsonify(booking_facade.fazer_checkin(res_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/reservations/<res_id>/cancel")
def cancel_reservation(res_id):
    try:
        data = request.get_json() or {}
        return jsonify(booking_facade.cancelar(
            booking_id=res_id,
            tempo_antecedencia_horas=data.get("tempo_antecedencia_horas", 24),
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/reservations/<res_id>/reminder")
def create_reminder(res_id):
    try:
        data = request.get_json() or {}
        return jsonify(booking_facade.agendar_lembrete(
            booking_id=res_id,
            user_id=data.get("user_id", "demo_user"),
            horas_antes=data.get("horas_antes", 24),
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Filtro de quadras ──────────────────────────────────────────────────────
@app.get("/api/quadras/filtro")
def filter_quadras():
    try:
        local = request.args.get("local")
        esporte = request.args.get("esporte")
        preco_maximo = request.args.get("preco_maximo", type=float)

        spaces = [
            SpaceBuilder(s.get("id", gen_id("s")), s["nome"])
                .com_esporte(s.get("modalidade", "Geral"))
                .com_localizacao(s.get("local", "Maceió"))
                .com_preco(100.0)
                .com_status("DISPONIVEL")
                .build()
            for s in SPACES
        ]

        resultado = filter_service.filtrar_avancado(
            spaces, local=local, esporte=esporte, preco_maximo=preco_maximo
        )

        return jsonify([{
            "nome": s.nome, "esporte": s.esporte,
            "localizacao": s.localizacao, "preco_hora": s.preco_hora,
            "status": s.status,
        } for s in resultado])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
