# MiteScan - Back-end

Esse repositório contém o back-end do projeto MiteScan, que está sendo desenvolvido em Python.

---

## Inicializando o Projeto

### Clonando o repositório

Clone o repositório para sua máquina utilizando:

```bash
git clone (url do repositório)
```

### Para inicializar o Docker

1. No seu computador, acesse o executor com Win + R e escreva "cmd".

2. Cole o código a seguir no terminal, caso necessário altere as informações:

```bash
docker run --name mitescan -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mitescan -p 5440:5432 -d postgres
```

3. Crie uma cópia do arquivo ".env.example", com o nome ".env" e atualize os dados de acordo com os de criação do Docker.

### Para inicializar a API

1. Dentro da IDE, no terminal do repositório, entre na pasta 'API' e execute os comandos a seguir:

```bash
python -m venv ./venv
```
Cria o arquivo da venv, que é um ambiente isolado para os pacotes usados no projeto.

```bash
./venv/Scripts/activate
```
Ativa o ambiente venv.

```bash
pip install -r requirements.txt
```
Instala todas as dependências do projeto contidas no arquivo requirements.txt.

2. Por fim, entre na pasta 'app' e rode o projeto com:

```bash
uvicorn main:app --reload
```

3. Quando terminar:

```bash
deactivate
```
Desativa o ambiente venv.
