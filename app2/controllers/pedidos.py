from io import BytesIO

from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, session, url_for
from openpyxl import Workbook
from openpyxl.styles import Font

from models import pedido as pedido_model
from models import prato as prato_model


pedido_bp = Blueprint("pedido", __name__, url_prefix="/pedidos")


def _carrinho():
    return session.setdefault("carrinho", [])


@pedido_bp.get("")
def listar():
    usuario_id = session["usuario_id"] if session.get("tipo_acesso") == "CLIENTE" else None
    return render_template("pedidos.html", pedidos=pedido_model.listar(usuario_id))


@pedido_bp.get("/kds")
def fila_kds():
    if session.get("tipo_acesso") not in ["COZINHEIRO", "ADMIN"]:
        flash("Acesso permitido apenas para a equipe da cozinha.", "erro")
        return redirect(url_for("main.inicio"))
    return render_template("kds.html", pedidos=pedido_model.listar_fila_kds())


@pedido_bp.post("/<int:pedido_id>/status")
def atualizar_status(pedido_id):
    if session.get("tipo_acesso") not in ["COZINHEIRO", "ADMIN"]:
        flash("Ação não permitida.", "erro")
        return redirect(url_for("main.inicio"))
    novo_status = request.form.get("status", "")
    if novo_status in ["Aguardando", "Em Preparo", "Pronto", "Entregue"]:
        pedido_model.atualizar_status(pedido_id, novo_status)
        flash("Status do pedido atualizado.", "sucesso")
    return redirect(url_for("pedido.fila_kds"))


@pedido_bp.get("/nova")
def nova():
    carrinho = _carrinho()
    total = sum(i["preco_centavos"] * i["quantidade"] for i in carrinho)
    return render_template("carinho.html", pratos=prato_model.listar(), carrinho=carrinho, total=total)


@pedido_bp.post("/carrinho/adicionar")
def adicionar():
    try:
        prato_id = int(request.form.get("prato_id", ""))
        quantidade = int(request.form.get("quantidade", ""))
    except ValueError:
        prato_id, quantidade = 0, 0
    prato = prato_model.buscar(prato_id)
    if prato is None or quantidade <= 0:
        flash("Selecione um prato e uma quantidade válida.", "erro")
    elif quantidade > prato["estoque"]:
        flash("A quantidade supera o estoque disponível.", "erro")
    else:
        carrinho = _carrinho()
        existente = next((i for i in carrinho if i["prato_id"] == prato_id), None)
        nova_quantidade = quantidade + (existente["quantidade"] if existente else 0)
        if nova_quantidade > prato["estoque"]:
            flash("A quantidade total no carrinho supera o estoque.", "erro")
            return redirect(url_for("pedido.nova"))
        if existente:
            existente["quantidade"] = nova_quantidade
        else:
            carrinho.append({"prato_id": prato["id"], "nome": prato["nome"],
                             "preco_centavos": prato["preco_centavos"], "quantidade": quantidade})
        session["carrinho"] = carrinho
        flash("Prato adicionado ao carrinho.", "sucesso")
    return redirect(url_for("pedido.nova"))


@pedido_bp.post("/carrinho/<int:indice>/remover")
def remover(indice):
    carrinho = _carrinho()
    if indice < 0 or indice >= len(carrinho):
        abort(404)
    carrinho.pop(indice)
    session["carrinho"] = carrinho
    return redirect(url_for("pedido.nova"))


@pedido_bp.post("/carrinho/limpar")
def limpar():
    session.pop("carrinho", None)
    flash("Carrinho esvaziado.", "sucesso")
    return redirect(url_for("pedido.nova"))


@pedido_bp.post("/finalizar")
def finalizar():
    carrinho = _carrinho()
    if not carrinho:
        flash("O carrinho está vazio.", "erro")
        return redirect(url_for("pedido.nova"))
    try:
        pedido_id = pedido_model.finalizar(session["usuario_id"], carrinho)
    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("pedido.nova"))
    session.pop("carrinho", None)
    flash("Pedido realizado com sucesso.", "sucesso")
    return redirect(url_for("pedido.detalhes", pedido_id=pedido_id))


@pedido_bp.get("/<int:pedido_id>")
def detalhes(pedido_id):
    pedido = pedido_model.buscar(pedido_id)
    if pedido is None:
        abort(404)
    return render_template("detalhes_pedido.html", pedido=pedido,
                           itens=pedido_model.listar_itens(pedido_id))


@pedido_bp.get("/exportar")
def exportar():
    wb = Workbook()
    ws = wb.active
    ws.title = "Pedidos"
    ws.append(["Código", "Data e hora", "Cliente", "Status", "Total (R$)"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for p in pedido_model.listar():
        ws.append([p["id"], p["criado_em"], p["usuario_nome"], p["status"], p["total_centavos"]])
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 15
    for cell in ws["E"][1:]:
        cell.number_format = 'R$ #,##0.00'
    arquivo = BytesIO()
    wb.save(arquivo)
    arquivo.seek(0)
    return send_file(arquivo, as_attachment=True, download_name="pedidos_sabor_e_clic.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")