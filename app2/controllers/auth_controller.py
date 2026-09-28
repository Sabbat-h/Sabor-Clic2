from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import usuario as usuario_model


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        usuario_input = request.form.get("usuario", "").strip()
        senha_input = request.form.get("senha", "").strip()

        user = usuario_model.buscar_por_usuario(usuario_input)

        if user is None or not check_password_hash(user["senha_hash"], senha_input):
            flash("Usuário ou senha incorretos.", "erro")
        else:
            session.clear()
            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["nome"]

            tipo = user["tipo_acesso"] if "tipo_acesso" in user.keys() else "CLIENTE"
            session["tipo_acesso"] = tipo or "CLIENTE"

            flash(f"Bem-vindo(a), {user['nome']}!", "sucesso")
            return redirect(url_for("main.inicio"))

    return render_template("login.html")


@auth_bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        usuario_input = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()
        tipo_acesso = request.form.get("tipo_acesso", "CLIENTE").strip().upper()

        if not nome or not usuario_input or not senha:
            flash("Preencha todos os campos obrigatórios.", "erro")
        elif usuario_model.buscar_por_usuario(usuario_input) is not None:
            flash("Nome de usuário já cadastrado.", "erro")
        else:
            senha_hash = generate_password_hash(senha)
            usuario_model.criar(nome, usuario_input, senha_hash, tipo_acesso)
            flash("Conta criada com sucesso! Faça login.", "sucesso")
            return redirect(url_for("auth.login"))

    return render_template("cadastro_usuario.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "sucesso")
    return redirect(url_for("auth.login"))