import sqlite3

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()

# Criar tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")

cursor.execute("DROP TABLE IF EXISTS tarefas")

# Criar tabela de tarefas
cursor.execute("""
CREATE TABLE tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    prioridade TEXT,
    horario TEXT,
    data_criacao TEXT,
    concluida INTEGER,
    apagada INTEGER DEFAULT 0,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

# Inserir usuários de exemplo
cursor.execute("DELETE FROM usuarios")
usuarios = [
    ("matheus", "senha123"),
    ("marcos", "123marcos"),
    ("miguel", "miguel2024")
]
cursor.executemany("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", usuarios)

conn.commit()
conn.close()
print("Banco de dados recriado com a coluna 'apagada' e usuários inseridos.")
