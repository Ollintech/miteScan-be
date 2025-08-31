# MiteScan 🐝

Sistema de monitoramento inteligente para colmeias, desenvolvido para auxiliar apicultores no controle e análise de suas colmeias através de sensores IoT e análise de dados.

## 📋 Sobre o Projeto

O MiteScan é uma solução completa que combina hardware (sensores e câmeras) com software (API REST e análise de dados) para monitoramento em tempo real de colmeias. O sistema permite:

- Monitoramento de temperatura e umidade das colmeias
- Análise de imagens para detecção de pragas (ácaros)
- Gestão de múltiplas colmeias por usuário
- Sistema de alertas via MQTT
- Interface web para visualização de dados

## 🏗️ Arquitetura do Projeto

```
MiteScan/
├── API/                    # Backend da aplicação
│   ├── app/               # Código principal da API Flask
│   │   ├── app.py         # Aplicação principal Flask
│   │   ├── run.py         # Script de inicialização
│   │   ├── mqtt_handler.py # Gerenciamento MQTT
│   │   ├── seed.py        # Dados iniciais do banco
│   │   ├── auth/          # Sistema de autenticação
│   │   ├── config/        # Configurações da aplicação
│   │   ├── models/        # Modelos SQLAlchemy
│   │   ├── routes/        # Rotas da API
│   │   └── tests/         # Testes automatizados
│   ├── requirements_flask.txt # Dependências Flask
│   └── .env.example       # Exemplo de configuração
├── bd/                    # Scripts do banco de dados
│   ├── mitescan_bd.sql   # Estrutura do banco
│   └── script.sql        # Scripts auxiliares
├── Periféricos/          # Código Arduino/IoT
│   ├── Analise-Algoritmica.ino  # Algoritmos de análise
│   ├── camera-MiteScan.ino      # Controle da câmera
│   └── sensores-MiteScan.ino    # Sensores de temperatura/umidade
└── README.md
```

## 🚀 Tecnologias Utilizadas

### Backend
- **Flask** - Framework web minimalista e flexível
- **Flask-SQLAlchemy** - ORM para Python
- **Flask-JWT-Extended** - Autenticação JWT
- **Flask-CORS** - Suporte a CORS
- **PostgreSQL** - Banco de dados relacional
- **Paho-MQTT** - Cliente MQTT para comunicação IoT
- **Docker** - Containerização

### Hardware/IoT
- **Arduino** - Microcontrolador para sensores
- **Sensores de temperatura e umidade**
- **Câmera para análise de imagens**
- **Protocolo MQTT** - Comunicação entre dispositivos

## 📦 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- PostgreSQL
- Arduino IDE (para programação dos sensores)

## 🛠️ Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd MiteScan
```

### 2. Configuração do Banco de Dados (Docker)

Execute o comando abaixo para criar o container PostgreSQL:

```bash
docker run --name mitescan-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mitescan \
  -p 5440:5432 \
  -d postgres
```

### 3. Configuração do Ambiente

1. Crie um arquivo `.env` na pasta `API/` baseado no `.env.example`:

```bash
cd API
cp .env.example .env
```

2. Edite o arquivo `.env` com suas configurações:

```env
# Flask Configuration
SECRET_KEY=sua-chave-secreta-muito-segura
JWT_SECRET_KEY=sua-chave-jwt-muito-segura

# Database Configuration
DATABASE_URL=postgresql://admin:password@localhost:5440/mitescan

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=mitescan/sensors
API_SENSOR_URL=http://localhost:8000/sensors/data

# Environment
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Instalação das Dependências

```bash
cd API
pip install -r requirements_flask.txt
```

### 5. Configuração do Banco de Dados

Execute o script SQL para criar as tabelas:

```bash
psql -h localhost -p 5440 -U admin -d mitescan -f ../bd/mitescan_bd.sql
```

### 6. Executar a Aplicação

#### Opção 1: Usando o script de inicialização
```bash
cd app
python run.py
```

#### Opção 2: Executando diretamente
```bash
cd app
python app.py
```

A API estará disponível em: `http://localhost:8000`

## 📡 Configuração dos Sensores

### Arduino/ESP32

1. Abra o Arduino IDE
2. Instale as bibliotecas necessárias:
   - DHT sensor library
   - PubSubClient (MQTT)
   - WiFi library

3. Configure os arquivos `.ino` na pasta `Periféricos/`:
   - `sensores-MiteScan.ino` - Para sensores de temperatura/umidade
   - `camera-MiteScan.ino` - Para captura de imagens
   - `Analise-Algoritmica.ino` - Para processamento local

4. Atualize as configurações de WiFi e MQTT nos arquivos

## 🔧 Uso da API

### Endpoints Principais

#### Autenticação
- `POST /users/register` - Registrar novo usuário
- `POST /users/login` - Login de usuário
- `GET /users/me` - Informações do usuário atual

#### Colmeias
- `GET /hives` - Listar colmeias
- `POST /hives` - Criar nova colmeia
- `GET /hives/{id}` - Obter colmeia específica
- `PUT /hives/{id}` - Atualizar colmeia
- `DELETE /hives/{id}` - Deletar colmeia

#### Sensores
- `POST /sensors/data` - Receber dados dos sensores
- `GET /sensors/data` - Obter dados dos sensores
- `GET /sensors/stats/{hive_id}` - Estatísticas dos sensores

#### Análises
- `GET /hive-analysis` - Listar análises
- `POST /hive-analysis` - Criar nova análise
- `GET /hive-analysis/types` - Tipos de análise disponíveis

### Exemplo de Uso

```python
import requests

# Login
response = requests.post("http://localhost:8000/users/login", 
                        json={"email": "admin@mitescan.com", "password": "admin123"})
token = response.json()["access_token"]

# Headers de autenticação
headers = {"Authorization": f"Bearer {token}"}

# Listar colmeias
hives = requests.get("http://localhost:8000/hives", headers=headers)
print(hives.json())

# Enviar dados do sensor
sensor_data = {
    "hive_id": 1,
    "temperature": 25.5,
    "humidity": 60.2,
    "sensor_type": "DHT22"
}
response = requests.post("http://localhost:8000/sensors/data", json=sensor_data)
print(response.json())
```

## 🧪 Testes

Para executar os testes:

```bash
cd API/app
pip install pytest
python -m pytest tests/ -v
```

Para executar um teste específico:

```bash
python -m pytest tests/test_api.py::test_user_login -v
```

## 📊 Funcionalidades

### Sistema de Monitoramento
- ✅ Coleta de dados de temperatura e umidade
- ✅ Comunicação MQTT em tempo real
- ✅ Armazenamento histórico de dados
- ✅ Sistema de alertas
- ✅ API RESTful completa

### Gestão de Colmeias
- ✅ Cadastro de múltiplas colmeias
- ✅ Geolocalização das colmeias
- ✅ Tipos de abelhas personalizáveis
- ✅ Análise de dados históricos
- ✅ Estatísticas detalhadas

### Sistema de Usuários
- ✅ Autenticação JWT
- ✅ Níveis de acesso diferenciados
- ✅ Gestão por empresas
- ✅ Controle de sessões
- ✅ Middleware de segurança

### Análises e Relatórios
- ✅ Análise de imagens
- ✅ Detecção de pragas
- ✅ Backup de análises
- ✅ Relatórios de saúde das colmeias

## 🔄 Migração do FastAPI para Flask

Esta versão foi migrada do FastAPI para Flask, mantendo todas as funcionalidades:

### Principais Mudanças:
- **Framework**: FastAPI → Flask
- **ORM**: Mantido SQLAlchemy, adaptado para Flask-SQLAlchemy
- **Autenticação**: Pydantic + OAuth2 → Flask-JWT-Extended
- **Validação**: Pydantic → Marshmallow (opcional)
- **CORS**: FastAPI CORS → Flask-CORS
- **Estrutura**: Routers → Blueprints

### Vantagens do Flask:
- ✅ Maior flexibilidade e controle
- ✅ Ecossistema maduro e estável
- ✅ Melhor para projetos que precisam de customização
- ✅ Documentação extensa e comunidade ativa
- ✅ Integração mais simples com outras bibliotecas Python

## 📈 Monitoramento

O sistema inclui:
- Logs estruturados com diferentes níveis
- Métricas de performance da API
- Monitoramento de saúde dos sensores
- Alertas automáticos via MQTT
- Sistema de backup de análises

## 🐛 Debugging

Para debug avançado:

```bash
# Ativar modo debug
export FLASK_DEBUG=True

# Executar com logs detalhados
python app.py

# Testar MQTT separadamente
python mqtt_handler.py
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Equipe

- **Desenvolvimento Backend** - API Flask e integração MQTT
- **Desenvolvimento IoT** - Sensores e dispositivos Arduino
- **Banco de Dados** - Modelagem e otimização PostgreSQL

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no GitHub
- Entre em contato com a equipe de desenvolvimento

---

**MiteScan Flask** - Tecnologia a serviço da apicultura sustentável 🐝🌱