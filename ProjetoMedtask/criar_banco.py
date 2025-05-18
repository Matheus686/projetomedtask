import sqlite3

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    prioridade TEXT,
    horario TEXT,
    data_criacao TEXT,
    data_prevista TEXT,
    concluida INTEGER,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

cursor.execute("DELETE FROM usuarios")
usuarios = [
    ("matheus", "senha123"),
    ("marcos", "123marcos"),
    ("miguel", "miguel2024")
]
cursor.executemany("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", usuarios)

conn.commit()
conn.close()
print("Banco de dados criado com 3 usuários.")
