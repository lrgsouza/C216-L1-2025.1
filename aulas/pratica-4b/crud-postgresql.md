[Voltar ao início](../../README.md)
---

### Prática 4b - CRUD de Professores com PostgreSQL (asyncpg + FastAPI)

Nesta prática, vamos evoluir a API de professores criada na prática 4a para utilizar **persistência de dados com PostgreSQL**, usando `asyncpg` para comunicação assíncrona com o banco de dados.

---

### Pré-requisitos

- Docker: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Postman: [Download Postman](https://www.postman.com/downloads/)

---

### Endpoints da API:

- `POST /api/v1/professores/`: Cadastra um novo professor.
- `GET /api/v1/professores/`: Lista todos os professores.
- `GET /api/v1/professores/{professor_id}`: Busca um professor pelo ID.
- `PATCH /api/v1/professores/{professor_id}`: Atualiza dados de um professor.
- `DELETE /api/v1/professores/{professor_id}`: Remove um professor do sistema.
- `DELETE /api/v1/professores/`: Restaura o banco de dados com os professores iniciais.

---

### Script SQL de Inicialização (`backend/db/init.sql`)

```sql
DROP TABLE IF EXISTS professores;

CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sala_de_atendimento VARCHAR(50) NOT NULL
);

INSERT INTO professores (nome, email, sala_de_atendimento) VALUES 
('Professor 1', 'professor_1@example.com', 'Sala 101'),
('Professor 2', 'professor_2@example.com', 'Sala 102');
```

---

### Exemplo do código da API (FastAPI com asyncpg)


```python	
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
import time

app = FastAPI()

class Professor(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    sala_de_atendimento: str

class ProfessorAtualizar(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    sala_de_atendimento: Optional[str] = None

async def get_database():
    DATABASE_URL = os.getenv("PGURL", "postgres://postgres:postgres@db:5432/professores")
    return await asyncpg.connect(DATABASE_URL)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {duration:.4f}s")
    return response

@app.post("/api/v1/professores/", status_code=201)
async def criar_professor(professor: Professor):
    conn = await get_database()
    try:
        existe = await conn.fetchval("SELECT 1 FROM professores WHERE email=$1", professor.email)
        if existe:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        await conn.execute(
            "INSERT INTO professores (nome, email, sala_de_atendimento) VALUES ($1, $2, $3)",
            professor.nome, professor.email, professor.sala_de_atendimento
        )
        return {"message": "Professor cadastrado com sucesso!"}
    finally:
        await conn.close()

@app.get("/api/v1/professores/", response_model=List[Professor])
async def listar_professores():
    conn = await get_database()
    try:
        rows = await conn.fetch("SELECT * FROM professores ORDER BY id")
        return [dict(row) for row in rows]
    finally:
        await conn.close()

@app.get("/api/v1/professores/{professor_id}")
async def obter_professor(professor_id: int):
    conn = await get_database()
    try:
        prof = await conn.fetchrow("SELECT * FROM professores WHERE id=$1", professor_id)
        if not prof:
            raise HTTPException(status_code=404, detail="Professor não encontrado.")
        return dict(prof)
    finally:
        await conn.close()

@app.patch("/api/v1/professores/{professor_id}")
async def atualizar_professor(professor_id: int, dados: ProfessorAtualizar):
    conn = await get_database()
    try:
        prof = await conn.fetchrow("SELECT * FROM professores WHERE id=$1", professor_id)
        if not prof:
            raise HTTPException(status_code=404, detail="Professor não encontrado.")

        if dados.email:
            existe = await conn.fetchval(
                "SELECT 1 FROM professores WHERE email=$1 AND id<>$2", dados.email, professor_id)
            if existe:
                raise HTTPException(status_code=400, detail="Email já cadastrado.")

        await conn.execute("""
            UPDATE professores
            SET nome = COALESCE($1, nome),
                email = COALESCE($2, email),
                sala_de_atendimento = COALESCE($3, sala_de_atendimento)
            WHERE id = $4
        """, dados.nome, dados.email, dados.sala_de_atendimento, professor_id)
        return {"message": "Professor atualizado com sucesso!"}
    finally:
        await conn.close()

@app.delete("/api/v1/professores/{professor_id}")
async def remover_professor(professor_id: int):
    conn = await get_database()
    try:
        result = await conn.execute("DELETE FROM professores WHERE id=$1", professor_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Professor não encontrado.")
        return {"message": "Professor removido com sucesso!"}
    finally:
        await conn.close()

@app.delete("/api/v1/professores/")
async def resetar_professores():
    conn = await get_database()
    try:
        init_sql = os.getenv("INIT_SQL", "db/init.sql")
        with open(init_sql, 'r') as f:
            sql = f.read()
        await conn.execute(sql)
        return {"message": "Banco de dados restaurado com sucesso!"}
    finally:
        await conn.close()

```


--

### Modelos e Estrutura da API

A API utiliza `FastAPI` com `asyncpg`. Veja o conteúdo de `backend/main.py` para as operações de CRUD completas com conexão assíncrona ao PostgreSQL.

- Cada operação abre uma conexão com o banco via `get_database()`.
- As operações são envoltas em blocos `try/finally` para garantir que as conexões sejam fechadas.
- Um middleware exibe logs de cada requisição (método, rota e tempo).

---

### Docker e Execução da API

#### Dockerfile
```Dockerfile
# Usando uma imagem base do Python
FROM python:3.10-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando todo o conteúdo do diretório atual para o diretório /app no container
COPY . .

# Instalando dependências
RUN pip install -r requirements.txt

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### requirements.txt
```
fastapi
uvicorn
asyncpg
```

#### docker-compose.yml
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PGURL=postgres://postgres:postgres@db:5432/professores
      - INIT_SQL=db/init.sql
    depends_on:
      - db

  db:
    image: postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: professores
```

---

### Executando a API

1. Execute com Docker:
```bash
docker-compose up --build
```

2. Acesse a documentação:
```
http://localhost:8000/docs
```

---

### Exercício Proposto

1. Atualizar a API de **ALUNOS** para uso com PostgreSQL.
2. Executar a API com docker-compose (**obrigatório**).
3. Criar uma **collection** no Postman com os testes:
    - Reset do banco de dados
    - Cadastro de alunos (pelo menos 3 de cada curso)
    - Listagem geral
    - Busca por ID
    - Atualização parcial
    - Exclusão individual
    - Reset do banco de dados
4. Subir a collection em `pratica-4b/api-tests/`.
5. Tirar prints:
   - Logs do container
   - Resultados no Postman (SUMMARY)
   - Salvar em `pratica-4b/img/`.

## Observações Importantes

- O ID do aluno deve ser a marticula e a mesma sendo a chave primária, Se um aluno for deletado, o ID nao pode ser reutilizado.
- O ID deve ser composto pelo curso (GES, GEC, etc) e a matrícula do aluno (ex: GES1, GES2, GEC1, GEC2, etc).
- A matrícula deve ser única e não pode ser nula **POR CURSO**.
- O Projeto deve ter pelo menos 2 cursos diferentes (ex: GES e GEC).
- O CONTADOR GLOBAL DEVE SER PERSISTENTE, ou seja, se o aluno 1 for deletado, o aluno 2 não pode ser GES1 novamente.
- O ID deve ser gerado automaticamente, não pode ser enviado na requisição.


---

### Estrutura esperada para entrega: (Estrurura fora do padrão acarretará em desconto de 10 pontos)

```sh
 - aulas/
    - pratica-4b/
       - api-tests/
          - C216-L1-PRATICA-4b-Nome_Matricula.postman_collection.json
       - img/
          - logs-api.png
          - postman.png
 - backend/
    - db/
       - init.sql
    - main.py
    - Dockerfile
docker-compose.yml
```

---

[Voltar ao início](../../README.md)
