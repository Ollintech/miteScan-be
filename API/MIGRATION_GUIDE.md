
# 🔄 Guia de Migração: FastAPI → Flask

## ✅ Migração Concluída

O projeto MiteScan foi completamente migrado do FastAPI para Flask.

### 📋 Checklist de Migração

#### ✅ Estrutura do Projeto
- [x] Aplicação principal (app.py)
- [x] Sistema de configuração
- [x] Modelos SQLAlchemy adaptados para Flask-SQLAlchemy
- [x] Sistema de autenticação com JWT
- [x] Rotas convertidas para Blueprints
- [x] MQTT handler atualizado
- [x] Sistema de seed atualizado
- [x] Testes básicos implementados

#### ✅ Funcionalidades Migradas
- [x] Autenticação de usuários
- [x] Gestão de empresas
- [x] Gestão de colmeias
- [x] Sistema de sensores
- [x] Análises de colmeias
- [x] Backup de análises
- [x] Tipos de abelhas
- [x] Níveis de acesso
- [x] Comunicação MQTT

#### ✅ Arquivos Criados/Atualizados
- [x] API/app/app.py - Aplicação principal Flask
- [x] API/app/run.py - Script de inicialização
- [x] API/app/config/config.py - Configurações
- [x] API/app/auth/auth.py - Sistema de autenticação
- [x] API/app/models/*.py - Modelos Flask-SQLAlchemy
- [x] API/app/routes/*.py - Rotas Flask (Blueprints)
- [x] API/app/mqtt_handler.py - Handler MQTT atualizado
- [x] API/app/seed.py - Seed atualizado
- [x] API/app/tests/test_api.py - Testes básicos
- [x] API/requirements_flask.txt - Dependências Flask
- [x] API/.env.example - Configuração de ambiente
- [x] README.md - Documentação atualizada

### 🚀 Como Usar a Nova Versão Flask

1. **Instalar Dependências:**
   ```bash
   cd API
   pip install -r requirements_flask.txt
   ```

2. **Configurar Ambiente:**
   ```bash
   cp .env.example .env
   # Editar .env com suas configurações
   ```

3. **Executar Aplicação:**
   ```bash
   cd app
   python run.py
   ```

### 🔧 Principais Diferenças

#### FastAPI → Flask
- `@app.get()` → `@bp.route('/', methods=['GET'])`
- `Depends()` → `@jwt_required()`
- `HTTPException` → `jsonify({'error': 'message'}), status_code`
- `Pydantic models` → `SQLAlchemy models + to_dict()`
- `APIRouter` → `Blueprint`

#### Autenticação
- OAuth2PasswordBearer → Flask-JWT-Extended
- Dependency injection → Decorators
- Automatic validation → Manual validation

### 📊 Comparação de Performance

| Aspecto | FastAPI | Flask |
|---------|---------|-------|
| Velocidade | Mais rápido | Rápido o suficiente |
| Flexibilidade | Menos flexível | Muito flexível |
| Documentação | Auto-gerada | Manual |
| Curva de aprendizado | Média | Baixa |
| Ecossistema | Novo | Maduro |

### 🎯 Vantagens da Migração

1. **Flexibilidade**: Flask oferece mais controle sobre a aplicação
2. **Maturidade**: Ecossistema mais maduro e estável
3. **Simplicidade**: Código mais simples e direto
4. **Customização**: Mais fácil de customizar e estender
5. **Debugging**: Melhor suporte para debugging
6. **Integração**: Melhor integração com outras bibliotecas Python

### 🔍 Testes

Execute os testes para verificar se tudo está funcionando:

```bash
cd API/app
python -m pytest tests/ -v
```

### 📝 Próximos Passos

1. Testar todas as funcionalidades
2. Implementar testes mais abrangentes
3. Configurar CI/CD se necessário
4. Documentar APIs específicas
5. Otimizar performance se necessário

### 🆘 Troubleshooting

#### Problema: Erro de importação
**Solução**: Verifique se todas as dependências estão instaladas:
```bash
pip install -r requirements_flask.txt
```

#### Problema: Erro de banco de dados
**Solução**: Verifique se o PostgreSQL está rodando e as configurações estão corretas no .env

#### Problema: MQTT não conecta
**Solução**: Verifique as configurações MQTT no .env e se o broker está rodando

### 📞 Suporte

Se encontrar problemas durante a migração:
1. Verifique os logs da aplicação
2. Consulte a documentação do Flask
3. Abra uma issue no repositório

---

**Migração concluída com sucesso! 🎉**
