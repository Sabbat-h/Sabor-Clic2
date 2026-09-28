from database import get_db


def listar(usuario_id=None):
    if usuario_id:
        return get_db().execute(
            """SELECT p.*, u.nome AS usuario_nome
               FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id
               WHERE p.usuario_id = ?
               ORDER BY p.criado_em DESC, p.id DESC""",
            (usuario_id,),
        ).fetchall()
    return get_db().execute(
        """SELECT p.*, u.nome AS usuario_nome
           FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id
           ORDER BY p.criado_em DESC, p.id DESC"""
    ).fetchall()


def listar_fila_kds():
    return get_db().execute(
        """SELECT p.*, u.nome AS usuario_nome
           FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id
           WHERE p.status != 'Entregue'
           ORDER BY p.criado_em ASC"""
    ).fetchall()


def buscar(pedido_id):
    return get_db().execute(
        """SELECT p.*, u.nome AS usuario_nome
           FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id WHERE p.id = ?""",
        (pedido_id,),
    ).fetchone()


def listar_itens(pedido_id):
    return get_db().execute(
        "SELECT * FROM itens_pedido WHERE pedido_id = ? ORDER BY id", (pedido_id,)
    ).fetchall()


def atualizar_status(pedido_id, status):
    db = get_db()
    db.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
    db.commit()


def finalizar(usuario_id, carrinho):
    db = get_db()
    try:
        itens = []
        for item in carrinho:
            prato = db.execute(
                "SELECT * FROM pratos WHERE id = ?", (item["prato_id"],)
            ).fetchone()
            if prato is None:
                raise ValueError(f"O prato {item['nome']} não existe mais.")
            if prato["estoque"] < item["quantidade"]:
                raise ValueError(f"Estoque insuficiente para {prato['nome']}.")
            itens.append((prato, item["quantidade"]))

        total = sum(p["preco_centavos"] * qtd for p, qtd in itens)
        cursor = db.execute(
            "INSERT INTO pedidos (usuario_id, total_centavos, status) VALUES (?, ?, 'Aguardando')",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid
        for prato, quantidade in itens:
            subtotal = prato["preco_centavos"] * quantidade
            db.execute(
                """INSERT INTO itens_pedido
                   (pedido_id, prato_id, prato_nome, preco_unitario_centavos,
                    quantidade, subtotal_centavos) VALUES (?, ?, ?, ?, ?, ?)""",
                (pedido_id, prato["id"], prato["nome"],
                 prato["preco_centavos"], quantidade, subtotal),
            )
            db.execute(
                "UPDATE pratos SET estoque = estoque - ? WHERE id = ?",
                (quantidade, prato["id"]),
            )
        db.commit()
        return pedido_id
    except Exception:
        db.rollback()
        raise


def quantidade_total():
    return get_db().execute("SELECT COUNT(*) AS total FROM pedidos").fetchone()["total"]