"""Cria usuários internos no banco local, sem expor cadastro privilegiado no site."""
import getpass
import sqlite3
from werkzeug.security import generate_password_hash
from app import app
from database import get_db

def main():
    perfil = input("Perfil (ADMIN ou COZINHEIRO): ").strip().upper()
    if perfil not in {"ADMIN", "COZINHEIRO"}:
        raise SystemExit("Perfil inválido.")
    nome = input("Nome completo: ").strip()
    usuario = input("Usuário: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = getpass.getpass("Senha (mínimo 8 caracteres): ")
    confirmar = getpass.getpass("Confirme a senha: ")
    if not all((nome, usuario, email)) or "@" not in email or len(senha) < 8 or senha != confirmar:
        raise SystemExit("Dados inválidos ou senhas diferentes.")
    with app.app_context():
        try:
            db = get_db()
            db.execute("INSERT INTO usuarios(nome,usuario,email,senha_hash,tipo_acesso) VALUES (?,?,?,?,?)",
                       (nome, usuario, email, generate_password_hash(senha), perfil))
            db.commit()
        except sqlite3.IntegrityError:
            raise SystemExit("Usuário ou e-mail já cadastrado.")
    print("Usuário interno criado com sucesso.")

if __name__ == "__main__":
    main()
