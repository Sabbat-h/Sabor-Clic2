from flask import Blueprint, render_template

from models import pedido, prato


main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def inicio():
    return render_template(
        "menu.html", total_pratos=prato.quantidade_total(), total_pedidos=pedido.quantidade_total()
    )