# 🌲 Leitor do Bosque

> **Projeto Integrador - Tecnologia da Informação (UNIVESP)**
> 
> Uma plataforma de gamificação literária inspirada no **Bosque de Leitura do Parque do Carmo**, em Itaquera.

---

## 📖 Sobre o Projeto
O **Leitor do Bosque** é uma aplicação web desenvolvida para incentivar o hábito da leitura através de mecânicas de RPG (Role-Playing Game). O sistema permite que frequentadores do parque registrem suas leituras, transformando cada página lida em pontos de experiência (XP) e evoluindo seus níveis dentro da comunidade.

### 🎯 Objetivos
*   **Gamificação:** Transformar a leitura em uma jornada de progresso visual.
*   **Integração:** Facilitar o cadastro de obras através da **API do Google Books**.
*   **Comunidade:** Fomentar a cultura local através de um ranking de leitores da região de Itaquera.

---

## 🛠️ Tecnologias Utilizadas

### **Back-end**
*   **Python / Flask:** Framework principal para rotas e lógica de servidor.
*   **SQLite:** Banco de dados relacional para armazenamento de usuários e acervos.
*   **Jinja2:** Motor de templates para renderização dinâmica de dados.

### **Front-end**
*   **Bootstrap 5:** Estrutura de layout responsiva e componentes de UI.
*   **CSS3 Avançado:** Aplicação de *Glassmorphism*, efeitos de profundidade e variáveis dinâmicas.
*   **JavaScript (Vanilla):** Consumo de API externa e manipulação do DOM para busca em tempo real.

---

## 🚀 Funcionalidades Principais

*   **Autenticação Segura:** Sistema de login e cadastro com proteção de sessão.
*   **Busca via Google Books:** Importação automática de títulos, capas e contagem de páginas.
*   **Estante Gamificada:** Painel visual com barra de progresso e cálculo automático de nível.
*   **Ranking de Leitores:** Mural social que exibe os principais leitores baseados no XP acumulado.
*   **Validação de Dados:** Bloqueio de livros duplicados na estante para garantir a integridade da gamificação.

---

## 🔧 Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/leitor-do-bosque.git](https://github.com/seu-usuario/leitor-do-bosque.git)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Inicie o servidor:**
    ```bash
    python app.py
    ```
4.  **Acesse no navegador:**
    `http://127.0.0.1:5000`

---

## 🌳 O Local Inspirador
O projeto homenageia o **Bosque de Leitura do Parque do Carmo**, inaugurado em 2006, que oferece um acervo físico e digital gratuito para a população da Zona Leste de São Paulo.

---

## 👤 Desenvolvedor
*   **Nimai Senemo Herrera** – Estudante de TI (UNIVESP)

---

**Leitor do Bosque: Onde a natureza e a cultura se encontram em cada página.** 🌿✨