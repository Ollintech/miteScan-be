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
    # Cole aqui a URL de conexão do Supabase
    DATABASE_URL="postgres://postgres:[SUA-SENHA]@[HOST-DO-SUPABASE]:5432/postgres"

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

---

## 🧠 Rede Neural - IA para análise de imagens
Dentro do backend, temos um módulo de Inteligência Artificial desenvolvido para auxiliar apicultores na identificação de possíveis ameaças às colmeias, como a presença do ácaro varroa e deformações nas asas das abelhas.

Este projeto implementa uma Rede Neural Convolucional (CNN) desenvolvida manualmente utilizando PyTorch, sem o uso de modelos prontos como YOLO, com o objetivo de compreender e controlar todo o processo de aprendizado da IA.

### 🧠 Objetivo

Identificar, a partir de imagens, se uma abelha está:

- 🟢 Normal  
- 🔴 Com presença de varroa  
- 🟡 Com asas deformadas  

Este módulo complementa o sistema principal do MiteScan, que utiliza sensores IoT (temperatura e umidade) para detectar condições de risco na colmeia.

## 📊 Outputs e Métricas

Durante o treinamento, o sistema gera automaticamente arquivos de saída na pasta outputs/:

📁 Arquivos gerados
- best_model.pth → modelo treinado com melhor desempenho na validação
- training_graph.png → gráfico de acurácia (treino vs validação)
- confusion_matrix.png → matriz de confusão das previsões

## 📈 Gráfico de Treinamento

Gerado com a biblioteca Matplotlib, mostra a evolução da acurácia ao longo das épocas:

- Linha azul → acurácia de treino
- Linha laranja → acurácia de validação

Permite identificar:

- aprendizado do modelo
- overfitting
- estabilidade do treinamento

## 🔍 Matriz de Confusão

Gerada com Seaborn + Scikit-learn, permite visualizar:

- acertos por classe
- erros de classificação
- confusão entre categorias (ex: varroa vs normal)

Os valores são normalizados (0 a 1), representando porcentagens.

## ⚙️ Como Funciona

O fluxo da IA é dividido em três partes principais:

### 📥 Treinamento (`train.py`)

- Carrega as imagens do dataset
- Redimensiona e transforma em **tensores (matrizes numéricas)**
- Executa o treinamento da rede neural
- Calcula o erro da previsão
- Ajusta os pesos com **backpropagation**
- Salva o modelo treinado em `outputs/best_model.pth`

### 🧠 Arquitetura da Rede (`model/cnn.py`)

Define a estrutura da CNN:

- Camadas convolucionais (extração de características)
- Funções de ativação (ReLU)
- Camadas de pooling
- Camadas totalmente conectadas

A rede aprende padrões como:

- presença do ácaro varroa
- deformações nas asas
- características de abelhas saudáveis

### 🔍 Inferência (`predict.py`)

- Recebe uma imagem nova
- Aplica o mesmo pré-processamento do treino
- Carrega o modelo treinado (`best_model.pth`)
- Retorna a classificação com base nos padrões aprendidos


## 🔄 Fluxo do Sistema


Imagem → Tensor → CNN → Probabilidades → Classe


## 🧪 Tecnologias Utilizadas

- Python 3.x  
- PyTorch  
- Torchvision  
- Pillow  
- Matplotlib  
- Seaborn  
- Scikit-learn  
