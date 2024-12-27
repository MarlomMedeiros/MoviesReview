# Movie Rating API Project

## Descrição do Projeto

Este projeto tem como objetivo centralizar dados sobre filmes e avaliações, integrando uma API pública gratuita (OMDb API) com um banco de dados relacional. Ele é estruturado para permitir a criação e atualização de informações sobre filmes e avaliações, utilizando o framework FastAPI para a API e SQLAlchemy para interagir com o banco de dados SQLite.

## Funcionalidades

- **Cadastro de Filmes**: Adiciona filmes à base de dados, consumindo dados da OMDb API para preencher informações detalhadas como título, ano de lançamento, gênero, diretor, sinopse e poster.
- **Cadastro de Avaliações**: Permite a criação de avaliações para filmes, incluindo nome do avaliador, nota de 1 a 10 e um comentário opcional.
- **Consulta de Avaliações de um Filme**: Retorna todas as avaliações de um filme específico.
- **Atualização de Filmes**: Atualiza informações sobre um filme já existente no banco de dados, com base nos dados fornecidos.

## Estrutura de Dados

### Tabelas

- **Filmes**: 
  - **id** (Primary Key)
  - **imdb_id** (Identificador único do IMDb)
  - **title** (Título do filme)
  - **year** (Ano de lançamento)
  - **genre** (Gênero do filme)
  - **director** (Diretor do filme)
  - **plot** (Sinopse do filme)
  - **poster** (URL do poster do filme)
  - **created_at** (Data de criação)
  - **updated_at** (Data de atualização)

- **Avaliações**:
  - **id** (Primary Key)
  - **movie_id** (Foreign Key, relacionado ao filme)
  - **name** (Nome do avaliador)
  - **rate** (Nota de 1 a 10)
  - **description** (Comentário da avaliação)
  - **created_at** (Data de criação)

### Relacionamento entre as tabelas

- A tabela de **Avaliações** está relacionada à tabela de **Filmes** através da chave estrangeira `movie_id`.

## Tecnologias Utilizadas

- **FastAPI**: Framework para criação da API.
- **SQLAlchemy**: ORM para interação com o banco de dados SQLite.
- **OMDb API**: API pública utilizada para buscar dados sobre filmes.
- **Pydantic**: Biblioteca para validação e definição de modelos de dados.
- **SQLite**: Banco de dados utilizado para persistência dos dados.
- **dotenv**: Biblioteca para carregar variáveis de ambiente.

## Endpoints da API

### 1. Criar Filme

- **Método**: `POST`
- **URL**: `/movies/`
- **Corpo**: JSON com informações sobre o filme.
- **Resposta**: Detalhes do filme recém-criado, incluindo ID e informações da OMDb API.

Exemplo de requisição:

{
  "title": "Inception", 
  "year": 2010, 
  "genre": "Sci-Fi", 
  "director": "Christopher Nolan" 
}

### 2. Atualizar Filme

- **Método**: `PUT`
- **URL**: `/movies/{movie_id}`
- **Corpo**: JSON com as informações a serem atualizadas.
- **Resposta**: Detalhes do filme atualizado.

### 3. Criar Avaliação

- **Método**: `POST`
- **URL**: `/ratings/`
- **Corpo**: JSON com informações sobre a avaliação.
- **Resposta**: Detalhes da avaliação recém-criada.

Exemplo de requisição:

{
  "movie_id": 1, 
  "name": "John Doe", 
  "rate": 8, 
  "description": "Great movie!" 
}

### 4. Consultar Avaliações de um Filme

- **Método**: `GET`
- **URL**: `/movies/{movie_id}/ratings`
- **Resposta**: Lista de avaliações associadas ao filme.

## Arquivos e Estrutura

### main.py

Este arquivo contém a implementação da API FastAPI, as rotas para criação e atualização de filmes e avaliações, além da integração com o banco de dados SQLite.

### Banco de Dados

#### Esquema do banco de dados:

[Esquema do banco de dados no DBDesigner](https://dbdesigner.page.link/qVqE4es8Jz1pZ5V69)

## Como executar os scripts

Para executar os scripts desse projeto, siga os seguintes passos:

1. **Instalar as dependências**: Certifique-se de que o ambiente esteja preparado com as bibliotecas necessárias, como FastAPI, SQLAlchemy, Pydantic, e outros. Para instalar as dependências, execute:

   pip install -r requirements.txt

2. **Configuração do Banco de Dados**: A aplicação usa SQLite como banco de dados. Não é necessário realizar configurações avançadas para o SQLite, mas o banco de dados será criado automaticamente quando o primeiro acesso à API for realizado.

3. **Rodar a API**: Utilize o FastAPI para rodar o servidor de desenvolvimento localmente:

   uvicorn main:app --reload

   Isso fará a API ficar acessível em `http://127.0.0.1:8000`.

4. **Testar a API**: Use ferramentas como Postman ou Insomnia, ou faça requisições diretamente pelo navegador para testar os endpoints da API. Você também pode acessar a documentação interativa gerada automaticamente pelo FastAPI em `http://127.0.0.1:8000/docs`.

## Decisões Técnicas na Construção do Banco de Dados e Scripts

- **Uso de SQLite**: O banco de dados SQLite foi escolhido por ser simples e leve, sem a necessidade de configuração extra. É ideal para protótipos e pequenas aplicações, como esta.
- **Estrutura Relacional**: Foi adotado um modelo relacional com duas tabelas principais: Filmes e Avaliações. Essa estrutura facilita a organização e consultas eficientes, além de suportar facilmente a criação de novas funcionalidades.
- **SQLAlchemy**: Foi utilizado o SQLAlchemy como ORM (Object Relational Mapper) para facilitar a interação com o banco de dados, abstraindo a complexidade das operações SQL. Isso permite escrever código Python mais limpo e legível.
- **OMDb API**: A integração com a OMDb API permite preencher informações detalhadas sobre os filmes automaticamente. Isso minimiza a necessidade de inserção manual de dados e garante informações atualizadas.
- **FastAPI e Pydantic**: O uso de FastAPI proporciona a criação rápida de uma API robusta, enquanto o Pydantic é utilizado para garantir a validação de dados e garantir que o corpo das requisições esteja em conformidade com o esperado.

## Limitações e Melhorias Futuras

### Limitações

- **Capacidade do SQLite**: O SQLite é adequado para um projeto de pequeno porte, mas pode apresentar limitações de escalabilidade e desempenho em sistemas maiores ou com grande volume de dados.
- **Falta de autenticação**: A aplicação não possui mecanismos de autenticação, o que significa que qualquer usuário pode cadastrar e avaliar filmes. Para maior segurança, seria interessante adicionar autenticação via tokens JWT ou outro método de login.
- **Atualização de Dados de Filmes**: A API permite atualizar os dados de filmes, mas ela não reconsome a OMDb API para atualizar as informações automaticamente. Isso pode gerar inconsistências caso o título ou outros dados de um filme mudem.

### Melhorias Futuras

- **Suporte a mais fontes de dados**: Incluir outras fontes de dados de filmes além da OMDb API, como TMDb ou IMDB diretamente, para aumentar a precisão e variedade de informações.
- **Sistema de Autenticação**: Implementar um sistema de login e autenticação para que apenas usuários autenticados possam cadastrar e avaliar filmes, garantindo um controle mais rigoroso das interações.
- **Paginação de Avaliações**: Implementar paginação para o endpoint de avaliações, para melhorar o desempenho ao consultar filmes com muitas avaliações.
- **Suporte a mais tipos de dados**: Além de avaliações e filmes, poderiam ser adicionadas outras entidades, como gêneros, atores, diretores, etc., permitindo uma maior flexibilidade na consulta e gestão dos dados.
