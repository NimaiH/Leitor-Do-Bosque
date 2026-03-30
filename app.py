import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Configurações
app.secret_key = 'chave_secreta_do_bosque'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Rotas de Autenticação (USUÁRIOS) ---

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
            return redirect(url_for('home'))
        return "E-mail ou senha incorretos!"
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
            conexao.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Este e-mail já está cadastrado."
    return "Todos os campos são obrigatórios."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- Rotas principais (Estante de livros) ---

@app.route('/')
def home():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return render_template('index.html', livros=[], xp=0)

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    # Busca apenas os livros do usuário logado
    cursor.execute("SELECT titulo, paginas, capa, id FROM livros WHERE usuario_id = ?", (usuario_id,))
    lista_livros = cursor.fetchall()

    # Soma o XP apenas do usuário logado
    cursor.execute("SELECT SUM(paginas) FROM livros WHERE usuario_id = ?", (usuario_id,))
    resultado_xp = cursor.fetchone()
    xp_total = resultado_xp[0] if resultado_xp and resultado_xp[0] else 0
    conexao.close()

    return render_template('index.html', livros=lista_livros, xp=xp_total)

# --- Gerenciamento de Livros ---

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

    nome_foto = "padrão.jpg"
    if foto:
        nome_foto = foto.filename
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, paginas, capa, usuario_id) VALUES (?, ?, ?, ?)", 
                   (titulo, paginas, nome_foto, usuario_id))
    conexao.commit()
    conexao.close()

    return redirect(url_for('home'))

@app.route('/deletar_livro/<int:id>')
def deletar_livro(id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    # Segurança: Só deleta se o livro pertencer ao usuário logado
    cursor.execute("DELETE FROM livros WHERE id = ? AND usuario_id = ?", (id, usuario_id))
    conexao.commit()
    conexao.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)