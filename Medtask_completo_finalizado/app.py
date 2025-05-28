from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
from datetime import datetime
import subprocess

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

def conectar():
    conn = sqlite3.connect("tarefas.db")
    conn.row_factory = sqlite3.Row
    return conn

def corrigir_horario(entrada):
    entrada = entrada.strip().replace(":", "")
    if not entrada.isdigit():
        return "00:00"
    entrada = entrada.zfill(4)
    return f"{entrada[:2]}:{entrada[2:]}"

@app.before_request
def carregar_usuario():
    g.usuario = None
    if "usuario_id" in session:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (session["usuario_id"],))
        g.usuario = cursor.fetchone()
        conn.close()

@app.route("/")
def index():
    erro = request.args.get("erro")
    return render_template("login.html", erro=erro)

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
        return redirect(url_for("index", erro=1))

@app.route("/menu")
def menu():
    if "usuario_id" not in session:
        return redirect(url_for("index"))
    return render_template("menu.html", nome=session["usuario_nome"])

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
    cursor.execute("""
        SELECT * FROM tarefas 
        WHERE usuario_id=? AND concluida = 0 AND apagada = 0
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
    return render_template("listar.html", tarefas=tarefas)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        prioridade_input = request.form["prioridade"]

        prioridade = {
            "1": "Alta",
            "2": "Média",
            "3": "Baixa"
        }.get(prioridade_input, "Desconhecida")

        horario_input = request.form["horario"]
        horario = corrigir_horario(horario_input)
        data_criacao = datetime.now()

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tarefas (titulo, prioridade, horario, data_criacao, concluida, apagada, usuario_id)
            VALUES (?, ?, ?, ?, 0, 0, ?)
        """, (titulo, prioridade, horario, data_criacao.strftime("%d-%m-%Y"), session["usuario_id"]))
        conn.commit()
        conn.close()

        flash("Tarefa cadastrada com sucesso!")
        return redirect(url_for("cadastrar"))

    return render_template("cadastrar.html")

@app.route("/deletar/<int:id>")
def deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id=? AND usuario_id=?", (id, session["usuario_id"]))
    conn.commit()
    conn.close()
    flash("Tarefa deletada com sucesso!")
    return redirect(url_for("listar_tarefas"))

@app.route("/concluir/<int:id>")
def concluir(id):
    if "usuario_id" not in session:
        return redirect(url_for("index"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id=? AND usuario_id=?", (id, session["usuario_id"]))
    conn.commit()
    conn.close()
    flash("Tarefa concluída com sucesso!")
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

        prioridade = {
            "1": "Alta",
            "2": "Média",
            "3": "Baixa"
        }.get(prioridade_input, "Desconhecida")

        horario_input = request.form["horario"]
        horario = corrigir_horario(horario_input)

        cursor.execute("""
            UPDATE tarefas SET titulo=?, prioridade=?, horario=?
            WHERE id=? AND usuario_id=?
        """, (titulo, prioridade, horario, id, session["usuario_id"]))
        conn.commit()
        conn.close()
        flash("Tarefa editada com sucesso!")
        return redirect(url_for("listar_tarefas"))
    else:
        cursor.execute("SELECT * FROM tarefas WHERE id=? AND usuario_id=?", (id, session["usuario_id"]))
        tarefa = cursor.fetchone()
        conn.close()
        return render_template("editar.html", tarefa=tarefa)

@app.route("/executar_main_c")
def executar_main_c():
    try:
        resultado = subprocess.run(["./meuscript"], capture_output=True, text=True)
        saida = resultado.stdout
        return render_template("c_output.html", saida=saida)
    except Exception as e:
        return f"<p>Erro ao executar o script C: {e}</p>"

if __name__ == "__main__":
    app.run(debug=True)
