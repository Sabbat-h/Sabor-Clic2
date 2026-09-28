from io import BytesIO

from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, session, url_for
from openpyxl import Workbook
from openpyxl.styles import Font

from models import prato as prato_model
from utils import moeda_para_centavos


prato_bp = Blueprint("prato", __name__, url_prefix="/pratos")


def _dados_formulario():
    nome = request.form.get("nome", "").strip()
    categoria = request.form.get("categoria", "").strip()
    descricao = request.form.get("descricao", "").strip()
    estoque = int(request.form.get("estoque", "0"))
    preco = moeda_para_centavos(request.form.get("preco", ""))
    ativo = 1 if request.form.get("ativo") else 0
    if not nome or not categoria or estoque < 0 or preco < 0:
        raise ValueError("Preencha todos os campos válidos.")
    return nome, descricao, categoria, preco, estoque, ativo


@prato_bp.get("")
def listar():
    busca = request.args.get("busca", "")
    categoria = request.args.get("categoria", "")
    return render_template("cardapio.html", pratos=prato_model.listar(busca, categoria), busca=busca, categoria=categoria)


@prato_bp.route("/novo", methods=("GET", "POST"))
def novo():
    if session.get("tipo_acesso") != "ADMIN":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("prato.listar"))
    if request.method == "POST":
        try:
            prato_model.criar(*_dados_formulario())
            flash("Prato cadastrado com sucesso.", "sucesso")
            return redirect(url_for("prato.listar"))
        except (ValueError, TypeError):
            flash("Preencha preço e estoque com valores válidos.", "erro")
    return render_template("prato_form.html", prato=None)


@prato_bp.route("/<int:prato_id>/editar", methods=("GET", "POST"))
def editar(prato_id):
    if session.get("tipo_acesso") != "ADMIN":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("prato.listar"))
    prato = prato_model.buscar(prato_id)
    if prato is None:
        abort(404)
    if request.method == "POST":
        try:
            prato_model.atualizar(prato_id, *_dados_formulario())
            flash("Prato atualizado com sucesso.", "sucesso")
            return redirect(url_for("prato.listar"))
        except (ValueError, TypeError):
            flash("Preencha preço e estoque com valores válidos.", "erro")
    return render_template("prato_form.html", prato=prato)


@prato_bp.post("/<int:prato_id>/excluir")
def excluir(prato_id):
    if session.get("tipo_acesso") != "ADMIN":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("prato.listar"))
    if prato_model.buscar(prato_id) is None:
        abort(404)
    prato_model.excluir(prato_id)
    flash("Prato excluído.", "sucesso")
    return redirect(url_for("prato.listar"))


@prato_bp.get("/exportar")
def exportar():
    wb = Workbook()
    ws = wb.active
    ws.title = "Cardápio"
    ws.append(["Código", "Nome", "Categoria", "Descrição", "Preço (R$)", "Estoque"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for p in prato_model.listar():
        ws.append([p["id"], p["nome"], p["categoria"], p["descricao"], p["preco_centavos"], p["estoque"]])
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 20
    for cell in ws["E"][1:]:
        cell.number_format = 'R$ #,##0.00'
    arquivo = BytesIO()
    wb.save(arquivo)
    arquivo.seek(0)
    return send_file(arquivo, as_attachment=True, download_name="cardapio_sabor_e_clic.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")