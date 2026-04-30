import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session


def buscar_dados_google(titulo):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{titulo}"
        resposta = requests.get(url, timeout=5)

        if resposta.status_code == 200:
            dados = resposta.json()
            if "items" in dados:
                info = dados["items"][0]["volumeInfo"]
                # 🖼️ CAPTURA DA CAPA: Tentamos pegar a imagem 'thumbnail'
                capa_url = info.get("imageLinks", {}).get("thumbnail", "")

                return {
                    "paginas_reais": info.get("pageCount", 0),
                    "titulo_oficial": info.get("title", titulo),
                    "capa_url": capa_url  # Nova informação!
                }
    except Exception as e:
        print(f"Erro na conexão externa: {e}")
    return None


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
        cursor.execute(
            "SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return redirect(url_for('estante'))

        return render_template('login.html', erro="E-mail ou senha incorretos. Tente novamente.")
    return render_template('login.html')

# ----------------- Cadastro de usuários -----------------#


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/salvar_usuario', methods=['POST'])
def salvar_usuario():
    # Coleta os dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    try:
        # Insere os dados na tabela do banco de dados
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)",
            (nome, email, senha)
        )
        conexao.commit()
    except sqlite3.IntegrityError:
        return "Erro: Este email já está registrado!"
    finally:
        conexao.close()

        # Redireciona para o login após o cadastro (Para o usuário fazer o login com o cadastro que ele acabou de fazer)
        return redirect(url_for('login'))


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
        "SELECT titulo, paginas, capa, id FROM livros WHERE usuario_id = ?", (usuario_id,))
    lista_livros = cursor.fetchall()
    cursor.execute(
        "SELECT SUM(paginas) FROM livros WHERE usuario_id = ?", (usuario_id,))
    resultado_xp = cursor.fetchone()
    xp_total = resultado_xp[0] if resultado_xp and resultado_xp[0] else 0
    conexao.close()
    return render_template('estante.html', livros=lista_livros, xp=xp_total)

# ─── CADASTRAR LIVRO (ROTA UNIFICADA) ──────────────────────────────────────────


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

    # Coleta os dados enviados pelo formulário (via campos ocultos e visíveis)
    titulo = request.form.get('titulo')
    paginas = request.form.get('paginas')
    capa_url = request.form.get('capa_url')

    if not capa_url or capa_url == "":
        capa_url = "padrao.jpg"

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO livros (titulo, paginas, capa, usuario_id) VALUES (?, ?, ?, ?)",
        (titulo, paginas, capa_url, usuario_id)
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
    cursor.execute(
        "DELETE FROM livros WHERE id = ? AND usuario_id = ?", (id, usuario_id))
    conexao.commit()
    conexao.close()
    return redirect(url_for('estante'))

# ─── RANKING ──────────────────────────────────────────────────────────────────

@app.route('/ranking')
def ranking():
    if not session.get('usuario_id'):
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    
    # Busca o nome, soma de páginas (XP) e contagem de livros lidos de cada usuário
    cursor.execute("""
        SELECT 
            u.nome, 
            SUM(l.paginas) as total_xp, 
            COUNT(l.id) as total_livros
        FROM usuarios u
        LEFT JOIN livros l ON u.id = l.usuario_id
        GROUP BY u.id
        ORDER BY total_xp DESC
    """)
    
    dados_ranking = cursor.fetchall()
    conexao.close()
    
    # Passamos o divisor de 300 e os dados para o ranking.html
    return render_template('ranking.html', ranking=dados_ranking, divisor=300)

#-----------------------------------------------------------------------#


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


if __name__ == '__main__':
    app.run(debug=True)
