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

    

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/cadastrar_livros')
def cadastrar_livros():
    return render_template('cadastrar_livros.html')



# Rota que recebe os dados do formulário
@app.route('/salvar_livro', methods=['POST'])
def salvar_livro():
    # Pegando os textos e foto do formulário
    titulo = request.form.get('titulo')
    paginas = request.form.get('paginas')
    foto = request.files.get('capa')

    #caso o usuário não envie foto
    nome_foto = "padrão.jpg" 
    if foto:
        nome_foto = foto.filename
        caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(caminho_foto)

    #Salvando no banco de dados
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, paginas, capa) VALUES (?, ?, ?)",
                   (titulo, paginas, nome_foto))
    conexao.commit()
    conexao.close()

    # Redireciona de volta para a página inicial
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)