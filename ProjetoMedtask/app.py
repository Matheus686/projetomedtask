from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

def conectar():
    return sqlite3.connect("tarefas.db")

def corrigir_horario(entrada):
    entrada = entrada.strip().replace(":", "")
    if not entrada.isdigit():
        return "00:00"
    entrada = entrada.zfill(4)
    return f"{entrada[:2]}:{entrada[2:]}"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["usuario_id"] = user[0]
        session["usuario_nome"] = usuario
        return redirect(url_for("menu"))
    else:
        return "Login inválido"

@app.route("/menu")
def menu():
    if "usuario_id" not in session:
        return redirect(url_for("index"))
    return render_template("menu.html", nome=session['usuario_nome'])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/tarefas")
def listar_tarefas():
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    conn = conectar()
    cursor = conn.cursor()
    
    # Ordenar por prioridade personalizada: Alta, Média, Baixa
    cursor.execute("""
        SELECT * FROM tarefas 
        WHERE usuario_id=? 
        ORDER BY 
            CASE prioridade
                WHEN 'Alta' THEN 1
                WHEN 'Média' THEN 2
                WHEN 'Baixa' THEN 3
                ELSE 4
            END,
            id ASC
    """, (session["usuario_id"],))

    tarefas = cursor.fetchall()
    conn.close()
    return render_template("tarefas.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    titulo = request.form["titulo"]
    prioridade_input = request.form["prioridade"]
    if prioridade_input == "1":
        prioridade = "Alta"
    elif prioridade_input == "2":
        prioridade = "Média"
    elif prioridade_input == "3":
        prioridade = "Baixa"
    else:
        prioridade = "Desconhecida"

    horario_input = request.form["horario"]
    horario = corrigir_horario(horario_input)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarefas (titulo, prioridade, horario, data_criacao, data_prevista, concluida, usuario_id)
        VALUES (?, ?, ?, date('now'), date('now', '+3 days'), 0, ?)
    """, (titulo, prioridade, horario, session["usuario_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_tarefas"))

@app.route("/deletar/<int:id>")
def deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id=? AND usuario_id=?", (id, session["usuario_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_tarefas"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        titulo = request.form["titulo"]
        prioridade_input = request.form["prioridade"]
        if prioridade_input == "1":
            prioridade = "Alta"
        elif prioridade_input == "2":
            prioridade = "Média"
        elif prioridade_input == "3":
            prioridade = "Baixa"
        else:
            prioridade = "Desconhecida"

        horario_input = request.form["horario"]
        horario = corrigir_horario(horario_input)

        cursor.execute("""
            UPDATE tarefas SET titulo=?, prioridade=?, horario=?
            WHERE id=? AND usuario_id=?
        """, (titulo, prioridade, horario, id, session["usuario_id"]))
        conn.commit()
        conn.close()
        return redirect(url_for("listar_tarefas"))
    else:
        cursor.execute("SELECT * FROM tarefas WHERE id=? AND usuario_id=?", (id, session["usuario_id"]))
        tarefa = cursor.fetchone()
        conn.close()
        return render_template("editar.html", tarefa=tarefa)

if __name__ == "__main__":
    app.run(debug=True)
