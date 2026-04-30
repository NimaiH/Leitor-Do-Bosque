import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session

# ─── CONFIGURAÇÕES INICIAIS E VARIÁVEIS DE AMBIENTE ───────────────────────
# Boas Práticas: Definir chaves e configurações no topo facilita a manutenção.
app = Flask(__name__)
app.secret_key = 'chave_secreta_do_bosque'

# 🎓 NOTA DE ESTUDO: Removemos o UPLOAD_FOLDER e os comandos de os.path aqui,
# pois agora dependemos exclusivamente de URLs externas da API do Google[cite: 2, 4].

# ─── SERVIÇOS EXTERNOS (API DO GOOGLE BOOKS) ──────────────────────────────
# Este bloco isola a comunicação com a internet.
def buscar_dados_google(titulo):
    """
    Consome a API do Google para buscar metadados de livros.
    Retorna um dicionário com páginas, título oficial e URL da capa[cite: 2].
    """
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{titulo}"
        resposta = requests.get(url, timeout=5)

        if resposta.status_code == 200:
            dados = resposta.json()
            if "items" in dados:
                info = dados["items"][0]["volumeInfo"]
                # 🖼️ CAPTURA DA CAPA: Retornamos o link direto da imagem
                capa_url = info.get("imageLinks", {}).get("thumbnail", "")

                return {
                    "paginas_reais": info.get("pageCount", 0),
                    "titulo_oficial": info.get("title", titulo),
                    "capa_url": capa_url
                }
    except Exception as e:
        print(f"Erro na conexão externa: {e}")
    return None

# ─── GERENCIAMENTO DE ACESSO (AUTENTICAÇÃO) ──────────────────────────────
# Bloco responsável por Login, Cadastro e Logout de usuários.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        conexao = sqlite3.connect('livros.db')
        cursor = conexao.cursor()
        # 🔐 SEGURANÇA: Buscamos o usuário no banco via SQL
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            # Sessões mantêm o usuário logado entre diferentes páginas
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return redirect(url_for('estante'))

        return render_template('login.html', erro="E-mail ou senha incorretos.")
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/salvar_usuario', methods=['POST'])
def salvar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)", (nome, email, senha))
        conexao.commit()
    except sqlite3.IntegrityError:
        return "Erro: Este email já está registrado!"
    finally:
        conexao.close()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão por segurança
    return redirect(url_for('sobre'))

# ─── PÁGINAS PRINCIPAIS (VISUALIZAÇÃO) ───────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/estante')
def estante():
    """ Página onde o usuário vê sua coleção e XP[cite: 3]. """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    # Buscamos livros e calculamos a soma de páginas (XP)[cite: 2, 4]
    cursor.execute("SELECT titulo, paginas, capa, id FROM livros WHERE usuario_id = ?", (usuario_id,))
    lista_livros = cursor.fetchall()
    cursor.execute("SELECT SUM(paginas) FROM livros WHERE usuario_id = ?", (usuario_id,))
    resultado_xp = cursor.fetchone()
    xp_total = resultado_xp[0] if resultado_xp and resultado_xp[0] else 0
    conexao.close()
    
    return render_template('estante.html', livros=lista_livros, xp=xp_total)

@app.route('/ranking')
def ranking():
    """ Sistema de comparação entre usuários baseada no XP. """
    if not session.get('usuario_id'):
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    # SQL avançado: Une as tabelas de usuários e livros para somar o XP de todos[cite: 5]
    cursor.execute("""
        SELECT u.nome, SUM(l.paginas) as total_xp, COUNT(l.id) as total_livros
        FROM usuarios u
        LEFT JOIN livros l ON u.id = l.usuario_id
        GROUP BY u.id
        ORDER BY total_xp DESC
    """)
    dados_ranking = cursor.fetchall()
    conexao.close()
    return render_template('ranking.html', ranking=dados_ranking, divisor=300)

# ─── OPERAÇÕES DE DADOS (CRUD - CREATE/DELETE) ───────────────────────────

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
    capa_url = request.form.get('capa_url')

    # ─── VALIDAÇÃO ANTI-DUPLICIDADE (Boas Práticas) ─────────────────────
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    # Verificamos se este usuário já cadastrou este título exato
    cursor.execute("SELECT id FROM livros WHERE titulo = ? AND usuario_id = ?", (titulo, usuario_id))
    livro_existente = cursor.fetchone()

    if livro_existente:
        conexao.close()
        # Aqui você pode redirecionar com um aviso ou apenas ignorar
        # Em um sistema real, enviaríamos uma mensagem de "Livro já está na estante"
        return redirect(url_for('estante')) 

    # ─── SE NÃO FOR DUPLICADO, SALVAMOS ────────────────────────────────
    if not capa_url or capa_url == "":
        capa_url = "https://via.placeholder.com/150x200?text=Sem+Capa"

    cursor.execute("INSERT INTO livros (titulo, paginas, capa, usuario_id) VALUES (?, ?, ?, ?)",
                   (titulo, paginas, capa_url, usuario_id))
    conexao.commit()
    conexao.close()
    
    return redirect(url_for('estante'))

@app.route('/deletar_livro/<int:id>')
def deletar_livro(id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    # Deleta apenas se o livro pertencer ao usuário logado (Segurança!)[cite: 5]
    cursor.execute("DELETE FROM livros WHERE id = ? AND usuario_id = ?", (id, usuario_id))
    conexao.commit()
    conexao.close()
    return redirect(url_for('estante'))

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

# ─── INICIALIZAÇÃO DO SERVIDOR ───────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)