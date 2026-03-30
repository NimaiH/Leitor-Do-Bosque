import sqlite3

def criar_banco():
    # Conecta ao arquivo do banco
    conexao = sqlite3.connect('livros.db')
    cursor = conexao.cursor()

        # NOVA: Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de Livros (Já existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            paginas INTEGER,
            capa TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas 'livros' e 'usuarios' prontos!") 

if __name__ == '__main__':
    criar_banco()