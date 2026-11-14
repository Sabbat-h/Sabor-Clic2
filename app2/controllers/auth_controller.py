import re
import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import usuario as usuario_model


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        usuario_input = request.form.get("usuario", "").strip()
        senha_input = request.form.get("senha", "").strip()

        user = (usuario_model.buscar_por_email(usuario_input.lower()) if "@" in usuario_input else usuario_model.buscar_por_usuario(usuario_input))

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
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()
        tipo_acesso = "CLIENTE"  # Cadastro público nunca define privilégios.
        confirmar_senha = request.form.get("confirmar_senha", senha)

        if not nome or not usuario_input or not senha or not email:
            flash("Preencha todos os campos obrigatórios.", "erro")
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email) or len(email) > 254:
            flash("Digite um e-mail válido com @ e domínio, como usuario@gmail.com.", "erro")
        elif senha != confirmar_senha:
            flash("As senhas não coincidem.", "erro")
        elif usuario_model.buscar_por_usuario(usuario_input) is not None:
            flash("Nome de usuário já cadastrado.", "erro")
        elif usuario_model.buscar_por_email(email) is not None:
            flash("E-mail já cadastrado.", "erro")
        else:
            senha_hash = generate_password_hash(senha)
            try:
                usuario_model.criar(nome, usuario_input, senha_hash, tipo_acesso, email)
            except sqlite3.IntegrityError:
                flash("Nome de usuário ou e-mail já cadastrado.", "erro")
            else:
                flash("Conta criada com sucesso! Faça login.", "sucesso")
                return redirect(url_for("auth.login"))

    return render_template("cadastro_usuario.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "sucesso")
    return redirect(url_for("auth.login"))