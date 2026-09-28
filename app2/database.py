import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    
    schema = """
    DROP TABLE IF EXISTS itens_pedido;
    DROP TABLE IF EXISTS pedidos;
    DROP TABLE IF EXISTS pratos;
    DROP TABLE IF EXISTS usuarios;

    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        tipo_acesso TEXT NOT NULL DEFAULT 'CLIENTE'
    );

    CREATE TABLE pratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        categoria TEXT NOT NULL,
        preco_centavos INTEGER NOT NULL,
        estoque INTEGER NOT NULL DEFAULT 0,
        ativo INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        total_centavos INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Aguardando',
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    );

    CREATE TABLE itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        prato_id INTEGER NOT NULL,
        prato_nome TEXT NOT NULL,
        preco_unitario_centavos INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        subtotal_centavos INTEGER NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
        FOREIGN KEY (prato_id) REFERENCES pratos (id)
    );
    """
    db.executescript(schema)
    db.commit()