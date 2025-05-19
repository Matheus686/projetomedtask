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

# Criar tabela de tarefas
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

# Inserir usuários
cursor.execute("DELETE FROM usuarios")
usuarios = [
    ("matheus", "senha123"),
    ("marcos", "123marcos"),
    ("miguel", "miguel2024")
]
cursor.executemany("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", usuarios)

# ✅ Correção das prioridades (Parte 1)
cursor.execute("UPDATE tarefas SET prioridade = 'Alta' WHERE LOWER(prioridade) = 'alta'")
cursor.execute("UPDATE tarefas SET prioridade = 'Média' WHERE LOWER(prioridade) = 'media'")
cursor.execute("UPDATE tarefas SET prioridade = 'Baixa' WHERE LOWER(prioridade) = 'baixa'")

conn.commit()
conn.close()
print("Banco de dados criado com 3 usuários e prioridades padronizadas.")
