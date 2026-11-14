import os
from decimal import Decimal

from flask import Flask, redirect, render_template, request, session, url_for

from database import close_db, init_db
from utils import centavos_para_moeda


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sabor_e_clic_secret_key_2026"
    app.config["DATABASE"] = os.path.join(app.root_path, "sabor_e_clic.sqlite")

    with app.app_context():
        init_db()

    from controllers.auth_controller import auth_bp
    from controllers.main_controller import main_bp
    from controllers.pedidos import pedido_bp
    from controllers.pratos_controller import prato_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(prato_bp)
    app.register_blueprint(pedido_bp)

    @app.before_request
    def verificar_autenticacao():
        # Revalida privilégios no banco a cada requisição autenticada.
        if session.get("usuario_id"):
            from models import usuario as usuario_model
            from database import get_db
            usuario = get_db().execute("SELECT tipo_acesso FROM usuarios WHERE id=?", (session["usuario_id"],)).fetchone()
            if usuario is None:
                session.clear()
            else:
                session["tipo_acesso"] = usuario["tipo_acesso"]
        rotas_publicas = {"auth.login", "auth.cadastro", "static", "prato.listar", "main.inicio", "main.agendamento"}
        if not session.get("usuario_id") and request.endpoint not in rotas_publicas:
            return redirect(url_for("auth.login"))

    @app.template_filter("moeda")
    def filtro_moeda(valor):
        return centavos_para_moeda(valor)

    @app.errorhandler(404)
    def pagina_nao_encontrada(e):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)