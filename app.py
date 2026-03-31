import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = 'chave_secreta_do_bosque'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ─── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        conexao = sqlite3.connect('livros.db')
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return redirect(url_for('estante'))

        return render_template('login.html', erro="E-mail ou senha incorretos. Tente novamente.")

    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/salvar_usuario', methods=['POST'])
def salvar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if nome and email and senha:
        try:
            conexao = sqlite3.connect('livros.db')
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conexao.commit()
            usuario_id = cursor.lastrowid
            conexao.close()
            session['usuario_id'] = usuario_id
            session['usuario_nome'] = nome
            return redirect(url_for('estante'))
        except sqlite3.IntegrityError:
            return render_template('cadastro.html', erro="Este e-mail ja esta cadastrado.")

    return render_template('cadastro.html', erro="Todos os campos sao obrigatorios.")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ─── LANDING PAGE ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')


# ─── ESTANTE ──────────────────────────────────────────────────────────────────

@app.route('/estante')
def estante():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT titulo, paginas, capa, id FROM livros WHERE usuario_id = ?",
        (usuario_id,)
    )
    lista_livros = cursor.fetchall()

    cursor.execute("SELECT SUM(paginas) FROM livros WHERE usuario_id = ?", (usuario_id,))
    resultado_xp = cursor.fetchone()
    xp_total = resultado_xp[0] if resultado_xp and resultado_xp[0] else 0

    conexao.close()
    return render_template('estante.html', livros=lista_livros, xp=xp_total)


# ─── CADASTRAR LIVRO ──────────────────────────────────────────────────────────

@app.route('/cadastrar_livros')
def cadastrar_livros():
    if not session.get('usuario_id'):
        return redirect(url_for('login'))
    return render_template('cadastrar_livros.html')


@app.route('/salvar_livro', methods=['POST'])
def salvar_livro():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    titulo = request.form.get('titulo')
    paginas = request.form.get('paginas')
    foto = request.files.get('capa')

    nome_foto = "padrao.jpg"
    if foto and foto.filename:
        nome_foto = foto.filename
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO livros (titulo, paginas, capa, usuario_id) VALUES (?, ?, ?, ?)",
        (titulo, paginas, nome_foto, usuario_id)
    )
    conexao.commit()
    conexao.close()

    return redirect(url_for('estante'))


# ─── DELETAR LIVRO ────────────────────────────────────────────────────────────

@app.route('/deletar_livro/<int:id>')
def deletar_livro(id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ? AND usuario_id = ?", (id, usuario_id))
    conexao.commit()
    conexao.close()

    return redirect(url_for('estante'))


# ─── SOBRE O BOSQUE ──────────────────────────────────────────────────────────

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# ─── INICIAR ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
