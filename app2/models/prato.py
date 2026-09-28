from database import get_db


def listar(busca="", categoria=""):
    termo = f"%{busca.strip()}%"
    cat = f"%{categoria.strip()}%"
    return get_db().execute(
        """SELECT * FROM pratos
           WHERE (nome LIKE ? OR descricao LIKE ?) AND categoria LIKE ?
           ORDER BY nome COLLATE NOCASE""",
        (termo, termo, cat),
    ).fetchall()


def buscar(prato_id):
    return get_db().execute("SELECT * FROM pratos WHERE id = ?", (prato_id,)).fetchone()


def criar(nome, descricao, categoria, preco_centavos, estoque, ativo=1):
    db = get_db()
    db.execute(
        """INSERT INTO pratos (nome, descricao, categoria, preco_centavos, estoque, ativo)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (nome, descricao, categoria, preco_centavos, estoque, ativo),
    )
    db.commit()


def atualizar(prato_id, nome, descricao, categoria, preco_centavos, estoque, ativo):
    db = get_db()
    db.execute(
        """UPDATE pratos SET nome=?, descricao=?, categoria=?, preco_centavos=?, estoque=?, ativo=?
           WHERE id=?""",
        (nome, descricao, categoria, preco_centavos, estoque, ativo, prato_id),
    )
    db.commit()


def excluir(prato_id):
    db = get_db()
    db.execute("DELETE FROM pratos WHERE id = ?", (prato_id,))
    db.commit()


def quantidade_total():
    return get_db().execute("SELECT COUNT(*) AS total FROM pratos").fetchone()["total"]