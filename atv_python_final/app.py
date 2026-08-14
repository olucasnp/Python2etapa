import os
from datetime import date
from functools import wraps

import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database as db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-secreta-dev-troque-em-producao")

_frase_cache = {"data": None, "frase": None}


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def buscar_frase_motivacional():
    """Busca uma frase motivacional na API pública adviceslip, com cache diário."""
    hoje = date.today().isoformat()
    if _frase_cache["data"] == hoje and _frase_cache["frase"]:
        return _frase_cache["frase"]

    try:
        resposta = requests.get("https://api.adviceslip.com/advice", timeout=3)
        resposta.raise_for_status()
        frase = resposta.json()["slip"]["advice"]
    except (requests.RequestException, KeyError, ValueError):
        frase = "Continue firme nas suas tarefas de hoje!"

    _frase_cache["data"] = hoje
    _frase_cache["frase"] = frase
    return frase


# ---------- autenticação ----------

@app.route("/")
def index():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("registro.html")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return render_template("registro.html")

        if db.buscar_usuario_por_email(email):
            flash("Este e-mail já está cadastrado.", "danger")
            return render_template("registro.html")

        senha_hash = generate_password_hash(senha)
        db.criar_usuario(nome, email, senha_hash)
        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = db.buscar_usuario_por_email(email)
        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))


# ---------- CRUD de tarefas ----------

@app.route("/dashboard")
@login_required
def dashboard():
    status_filtro = request.args.get("status")
    tarefas = db.listar_tarefas(session["usuario_id"], status_filtro)
    frase = buscar_frase_motivacional()
    return render_template(
        "dashboard.html", tarefas=tarefas, frase=frase, status_filtro=status_filtro or ""
    )


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título é obrigatório.", "danger")
            return render_template("form_tarefa.html", tarefa=None)

        if status not in db.STATUS_VALIDOS:
            status = "pendente"

        db.criar_tarefa(titulo, descricao, status, session["usuario_id"])
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("dashboard"))

    return render_template("form_tarefa.html", tarefa=None)


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_required
def editar_tarefa(tarefa_id):
    tarefa = db.buscar_tarefa(tarefa_id, session["usuario_id"])
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título é obrigatório.", "danger")
            return render_template("form_tarefa.html", tarefa=tarefa)

        if status not in db.STATUS_VALIDOS:
            status = "pendente"

        db.atualizar_tarefa(tarefa_id, session["usuario_id"], titulo, descricao, status)
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("dashboard"))

    return render_template("form_tarefa.html", tarefa=tarefa)


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
@login_required
def excluir_tarefa(tarefa_id):
    tarefa = db.buscar_tarefa(tarefa_id, session["usuario_id"])
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
    else:
        db.excluir_tarefa(tarefa_id, session["usuario_id"])
        flash("Tarefa removida.", "info")
    return redirect(url_for("dashboard"))


# ---------- dashboard de progresso ----------

@app.route("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")


@app.route("/api/progresso")
@login_required
def api_progresso():
    contagem = db.contar_tarefas_por_status(session["usuario_id"])
    return jsonify(contagem)


# ---------- API REST de tarefas (desafio avançado) ----------

def tarefa_para_dict(tarefa):
    return {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "status": tarefa["status"],
    }


@app.route("/api/tarefas", methods=["GET", "POST"])
@login_required
def api_tarefas():
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        titulo = str(dados.get("titulo", "")).strip()
        descricao = str(dados.get("descricao", "")).strip()
        status = dados.get("status", "pendente")

        if not titulo:
            return jsonify({"erro": "O título é obrigatório."}), 400
        if status not in db.STATUS_VALIDOS:
            status = "pendente"

        novo_id = db.criar_tarefa(titulo, descricao, status, session["usuario_id"])
        tarefa = db.buscar_tarefa(novo_id, session["usuario_id"])
        return jsonify(tarefa_para_dict(tarefa)), 201

    status_filtro = request.args.get("status")
    tarefas = db.listar_tarefas(session["usuario_id"], status_filtro)
    return jsonify([tarefa_para_dict(t) for t in tarefas])


@app.route("/api/tarefas/<int:tarefa_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_tarefa_detalhe(tarefa_id):
    tarefa = db.buscar_tarefa(tarefa_id, session["usuario_id"])
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    if request.method == "GET":
        return jsonify(tarefa_para_dict(tarefa))

    if request.method == "PUT":
        dados = request.get_json(silent=True) or {}
        titulo = str(dados.get("titulo", tarefa["titulo"])).strip()
        descricao = str(dados.get("descricao", tarefa["descricao"] or ""))
        status = dados.get("status", tarefa["status"])

        if not titulo:
            return jsonify({"erro": "O título é obrigatório."}), 400
        if status not in db.STATUS_VALIDOS:
            status = tarefa["status"]

        db.atualizar_tarefa(tarefa_id, session["usuario_id"], titulo, descricao, status)
        tarefa_atualizada = db.buscar_tarefa(tarefa_id, session["usuario_id"])
        return jsonify(tarefa_para_dict(tarefa_atualizada))

    db.excluir_tarefa(tarefa_id, session["usuario_id"])
    return jsonify({"sucesso": True})


if __name__ == "__main__":
    db.init_db()
    app.run(debug=False)
