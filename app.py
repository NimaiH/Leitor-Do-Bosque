import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuração para salvar as imagens enviadas
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria a pasta 'uploads' automaticamente se ela não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -----------------------------------------------------------------------------------------------------------#


# Função HOME

@app.route('/')
def home():
    # 1. Conectar ao banco de dados
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    # 2. Busca os dados necessários para os cards da estante
    # Pegando: Titulo (0), Paginas (1), Capa (2) e ID (3)
    cursor.execute("SELECT titulo, paginas, capa, id FROM livros")
    lista_livros = cursor.fetchall()

    # 3. Busca a soma de todas as páginas para calcular o XP total
    cursor.execute("SELECT SUM(paginas) FROM livros")
    resultado_xp = cursor.fetchone()

    # SUM retorna "none" se não conter nada nos dados então precisamos criar uma "regra" pra caso esse valor seja "none" mostrar 0 no site.
    xp_total = resultado_xp[0] if resultado_xp and resultado_xp[0] else 0

    # 5. Envia os livros e o XP para o index.html
    return render_template('index.html', livros=lista_livros, xp=xp_total)


# -----------------------------------------------------------------------------------------------------------#


# Cadastrar Livros

@app.route('/cadastrar_livros')
def cadastrar_livros():
    return render_template('cadastrar_livros.html')

# -----------------------------------------------------------------------------------------------------------#


# Rota que recebe os dados do formulário

@app.route('/salvar_livro', methods=['POST'])
def salvar_livro():
    # Pegando os textos e foto do formulário
    titulo = request.form.get('titulo')
    paginas = request.form.get('paginas')
    foto = request.files.get('capa')

    # Caso o usuário não envie foto.
    nome_foto = "padrão.jpg"
    if foto:
        nome_foto = foto.filename
        caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], nome_foto)
        foto.save(caminho_foto)

    # Salvando no banco de dados
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, paginas, capa) VALUES (?, ?, ?)",
                   (titulo, paginas, nome_foto))
    conexao.commit()
    conexao.close()

    # Voltar p/ pagina inicial.
    return redirect(url_for('home'))

# -----------------------------------------------------------------------------------------------------------#


# Função para Deletar Livros

@app.route('/deletar_livro/<int:id>')
def deletar_livro(id):
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    # Comando SQL para deletar baseado no ID único
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

    # Redireciona de volta para a home para atualizar a lista
    return redirect(url_for('home'))

# -----------------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    app.run(debug=True)
