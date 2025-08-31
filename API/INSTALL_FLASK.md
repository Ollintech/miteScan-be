# 🚀 Instruções de Instalação - MiteScan Flask

## ✅ Migração Concluída!

O projeto MiteScan foi **completamente migrado** do FastAPI para Flask! 🎉

## 📋 Próximos Passos para Usar

### 1. Instalar Dependências Flask

```bash
cd API
pip install -r requirements_flask.txt
```

### 2. Configurar Ambiente

```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar .env com suas configurações
# Exemplo de configuração mínima:
```

```env
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
JWT_SECRET_KEY=sua-chave-jwt-muito-segura-aqui
DATABASE_URL=postgresql://admin:password@localhost:5440/mitescan
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=mitescan/sensors
API_SENSOR_URL=http://localhost:8000/sensors/data
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Configurar Banco de Dados

```bash
# Iniciar PostgreSQL via Docker
docker run --name mitescan-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mitescan \
  -p 5440:5432 \
  -d postgres

# Executar script SQL
psql -h localhost -p 5440 -U admin -d mitescan -f bd/mitescan_bd.sql
```

### 4. Executar Aplicação

```bash
cd API/app
python run.py
```

**🌐 API disponível em: http://localhost:8000**

## 🧪 Testar a API

### Endpoints Principais:

```bash
# Health Check
curl http://localhost:8000/

# Registrar usuário
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste User",
    "email": "teste@mitescan.com",
    "password": "teste123",
    "access_id": 1,
    "company_id": 1
  }'

# Login
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mitescan.com",
    "password": "admin123"
  }'

# Enviar dados do sensor
curl -X POST http://localhost:8000/sensors/data \
  -H "Content-Type: application/json" \
  -d '{
    "hive_id": 1,
    "temperature": 25.5,
    "humidity": 60.2,
    "sensor_type": "DHT22"
  }'
```

## 📊 Funcionalidades Migradas

✅ **Sistema de Usuários**
- Registro e login
- Autenticação JWT
- Níveis de acesso

✅ **Gestão de Colmeias**
- CRUD completo
- Geolocalização
- Tipos de abelhas

✅ **Sistema de Sensores**
- Recepção de dados MQTT
- Armazenamento histórico
- Estatísticas

✅ **Análises**
- Backup de análises
- Análises de colmeias
- Tipos de análise

✅ **Comunicação MQTT**
- Cliente MQTT integrado
- Processamento em background
- Reconexão automática

## 🔧 Estrutura do Projeto Flask

```
API/app/
├── app.py              # Aplicação principal
├── run.py              # Script de inicialização
├── auth/               # Sistema de autenticação
├── config/             # Configurações
├── models/             # Modelos SQLAlchemy
├── routes/             # Rotas (Blueprints)
├── tests/              # Testes
├── mqtt_handler.py     # Handler MQTT
└── seed.py             # Dados iniciais
```

## 🎯 Vantagens da Migração

1. **🔧 Flexibilidade**: Mais controle sobre a aplicação
2. **📚 Maturidade**: Ecossistema estável e maduro
3. **🐛 Debugging**: Melhor suporte para debugging
4. **🔌 Integração**: Fácil integração com outras libs
5. **📖 Documentação**: Vasta documentação disponível

## 🆘 Troubleshooting

### Erro: ModuleNotFoundError
**Solução**: Instale as dependências
```bash
pip install -r requirements_flask.txt
```

### Erro: Database connection
**Solução**: Verifique se PostgreSQL está rodando
```bash
docker ps  # Verificar containers
```

### Erro: MQTT connection
**Solução**: Verifique configurações no .env
```bash
# Testar MQTT separadamente
python mqtt_handler.py
```

## 📞 Suporte

- 📖 Consulte: `API/MIGRATION_GUIDE.md`
- 🐛 Issues: Abra uma issue no GitHub
- 📧 Contato: Entre em contato com a equipe

---

**🎉 Migração Flask concluída com sucesso!**
**🚀 Pronto para usar a nova versão!**