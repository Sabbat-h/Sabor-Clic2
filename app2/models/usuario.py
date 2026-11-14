from database import get_db


def buscar_por_usuario(usuario):
    return get_db().execute(
        "SELECT * FROM usuarios WHERE usuario = ? COLLATE NOCASE", (usuario,)
    ).fetchone()


def buscar_por_email(email):
    return get_db().execute(
        "SELECT * FROM usuarios WHERE email = ? COLLATE NOCASE", (email,)
    ).fetchone()


def criar(nome, usuario, senha_hash, tipo_acesso="CLIENTE", email=None):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO usuarios (nome, usuario, senha_hash, tipo_acesso, email) VALUES (?, ?, ?, ?, ?)",
        (nome, usuario, senha_hash, tipo_acesso, email),
    )
    db.commit()
    return cursor.lastrowid