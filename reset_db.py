import os
from app import db, app

# Caminho para o banco SQLite
db_path = "local.db"

# Remover o banco antigo, se existir
if os.path.exists(db_path):
    os.remove(db_path)
    print("Banco de dados antigo removido.")

# Criar novamente o banco com a nova estrutura
with app.app_context():
    db.create_all()
    print("Novo banco de dados criado com sucesso.")
