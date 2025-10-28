# MiteScan - Backend

Este é o backend do projeto MiteScan, desenvolvido com FastAPI. Ele é responsável por gerenciar usuários, colmeias, receber dados de sensores via MQTT e fornecer uma API RESTful para o frontend.

## ✨ Funcionalidades

- **API RESTful**: Endpoints para gerenciamento de usuários, colmeias, tipos de abelha e análises.
- **Autenticação JWT**: Sistema de login seguro com tokens.
- **Integração MQTT**: Um serviço em background que escuta um broker MQTT, processa os dados recebidos dos sensores e os envia para a API.
- **ORM com SQLAlchemy**: Mapeamento objeto-relacional para interação com o banco de dados.
- **Seed de Dados**: Popula o banco de dados com dados iniciais na primeira execução.
- **Estrutura Organizada**: Código modularizado em rotas, schemas, modelos e serviços.

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento.

### 📋 Pré-requisitos

- **Python 3.9+**
- **Um banco de dados relacional** (PostgreSQL é recomendado).
- **Um Broker MQTT** (como [Mosquitto](https://mosquitto.org/download/)) instalado e rodando na sua rede.

### ⚙️ 1. Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/miteScan-be.git
    cd miteScan-be
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    > **Nota:** Certifique-se de ter um arquivo `requirements.txt` na raiz do projeto. Se não tiver, gere-o com `pip freeze > requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 2. Variáveis de Ambiente

1.  Na raiz do projeto, crie um arquivo chamado `.env`.

2.  Copie e cole o conteúdo abaixo no seu arquivo `.env`, **substituindo os valores com suas próprias configurações**.

    ```env
    # --- Configuração do Banco de Dados (Exemplo com PostgreSQL) ---
    # Formato: postgresql://<user>:<password>@<host>:<port>/<dbname>
    DATABASE_URL="postgresql://postgres:admin@localhost:5432/mitescan_db"

    # --- Configuração de Autenticação (JWT) ---
    # Gere uma chave segura (ex: usando `openssl rand -hex 32`)
    SECRET_KEY="SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # --- Configuração do MQTT ---
    # IP do computador onde o broker MQTT está rodando
    MQTT_BROKER="192.168.3.119"
    MQTT_PORT=1883
    # Tópico para escutar os dados dos sensores. O '#' é um coringa.
    MQTT_TOPIC="colmeia/#"

    # --- URL da API interna para o MQTT Handler ---
    # Endpoint que recebe os dados processados do sensor
    API_SENSOR_URL="http://127.0.0.1:8000/sensor"
    ```

### ▶️ 3. Executando a Aplicação

1.  **Inicie o servidor FastAPI:**
    A partir da raiz do projeto, execute:
    ```bash
    python app/main.py
    ```

2.  O servidor estará rodando em `http://localhost:8000`.

3.  Ao iniciar, a aplicação irá:
    - Criar as tabelas no banco de dados (se não existirem).
    - Popular o banco com dados iniciais (`seed_data`).
    - Iniciar o listener MQTT em um processo separado.

### 📚 4. Acessando a Documentação da API

Com o servidor rodando, você pode acessar a documentação interativa da API nos seguintes endereços:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Estrutura do Projeto

```
miteScan-be/
├── app/
│   ├── core/         # Configurações e lógica de autenticação
│   ├── db/           # Configuração do banco de dados
│   ├── models/       # Modelos SQLAlchemy (tabelas)
│   ├── routes/       # Endpoints da API (rotas)
│   ├── schemas/      # Schemas Pydantic (validação de dados)
│   ├── main.py       # Ponto de entrada da aplicação FastAPI
│   └── mqtt_handler.py # Lógica para o cliente MQTT
├── .env              # Arquivo de variáveis de ambiente (local)
└── README.md         # Este arquivo
```
