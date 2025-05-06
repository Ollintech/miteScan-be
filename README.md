# MiteScan - Back-end
Esse repositório contém o back-end do projeto MiteScan, que está sendo desenvolvido em Python.
<hr>
<h3>Inicializando o Projeto</h3>
- Clone o repositório para sua máquina utilizando:

`git clone (url do repositório)` <br>


<h4> Para inicializar o Docker:  </h4>

- No seu computador, acesse o executor com Win + R e escreva "cmd".

- Cole o código a seguir no terminal, caso necessário altere as informações.

`docker run --name meu-postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mitescan -p 5440:5432 -d postgres`


<h4> Para inicializar a API:  </h4>

- Dentro da IDE, no terminal do repositório, entre na pasta 'API' e execute os comandos a seguir:

  
`pip install -r requirements.txt` - Instala todas as dependências do projeto contidas no arquivo requirements.txt. <br>


- Entre na pasta 'app' e execute os comandos a seguir:


`python -m venv ./venv` - Cria o arquivo da venv, que é um ambiente isolado para os pacotes usados no projeto.<br>


`./venv/Scripts/activate` - Ativa o ambiente venv.<br>


<br>
Por fim, rode o projeto com:

`python app/main.py`

Quando terminar: 

`deactivate` - Para desativar o ambiente.<br>
