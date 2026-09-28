from database import get_db


def buscar_por_usuario(usuario):
    return get_db().execute(
        "SELECT * FROM usuarios WHERE usuario = ? COLLATE NOCASE", (usuario,)
    ).fetchone()


def criar(nome, usuario, senha_hash, tipo_acesso="CLIENTE"):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO usuarios (nome, usuario, senha_hash, tipo_acesso) VALUES (?, ?, ?, ?)",
        (nome, usuario, senha_hash, tipo_acesso),
    )
    db.commit()
    return cursor.lastrowid