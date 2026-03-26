
🌲 Leitor do Bosque
O Leitor do Bosque é uma plataforma web gamificada desenvolvida para incentivar o hábito da leitura. O projeto permite que usuários cadastrem seus livros, visualizem sua estante virtual e acompanhem seu progresso através de um sistema de XP (Experiência) baseado no número de páginas lidas.

Este software foi desenvolvido como parte do Projeto Integrador para o curso de Tecnologia da Informação da Univesp.



🚀 Funcionalidades
Estante Virtual: Visualização dinâmica de todos os livros cadastrados no banco de dados.

Gestão de Acervo: Cadastro de novos livros com título, número de páginas e upload de capa.

Sistema de Gamificação: Cálculo automático de XP total baseado na soma de páginas de todos os livros.

Progresso Visual: Barra de progresso dinâmica que indica o avanço do usuário em direção ao próximo nível.

Exclusão de Registros: Gerenciamento simples para remover livros da coleção.



🛠️ Tecnologias Utilizadas
Linguagem: Python 3.14+

Framework Web: Flask

Banco de Dados: SQLite3 (Relacional)

Front-End: HTML5, CSS3 e Bootstrap 5

Template Engine: Jinja2

Controle de Versão: Git & GitHub (seguindo padrões de Conventional Commits)



📂 Estrutura do Projeto

LEITOR-DO-BOSQUE/
├── static/
│   ├── uploads/       # Imagens das capas dos livros
│   └── style.css      # Estilização personalizada
├── templates/
│   ├── index.html     # Página principal (Estante e XP)
│   └── cadastrar_livros.html
├── app.py             # Lógica principal e rotas Flask
├── database.py        # Script de criação das tabelas SQLite
├── livros.db          # Arquivo do banco de dados (gerado automaticamente)
└── README.md



🔧 Como Executar o Projeto

1-- Clone o repositório:

git clone https://github.com/seu-usuario/leitor-do-bosque.git
cd leitor-do-bosque


2-- Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows


3--Instale as dependências:

pip install flask


4-- Prepare o banco de dados:

python database.py


5-- Execute a aplicação:

python app.py


Acesse no seu navegador: http://127.0.0.1:5000


📝 Notas de Desenvolvimento
O projeto utiliza o método SUM() do SQL para garantir eficiência no cálculo de experiência.

A interface foi desenhada com foco em UX, utilizando componentes responsivos do Bootstrap.

