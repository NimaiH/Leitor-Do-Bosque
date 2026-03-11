import sqlite3

def criar_banco():
    # Conecta ao arquivo do banco
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            paginas INTEGER,
            capa TEXT
    )

''')
    
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabela 'livros' criados com sucesso!") 

if __name__ == '__main__':
    criar_banco()