[Voltar ao início](../../README.md)
---

### Prática 4a - CRUD de Professores com Middleware

Nesta prática, vamos evoluir um programa simples de cadastro em terminal para uma API completa usando FastAPI, com o objetivo de gerenciar professores de uma universidade. A API seguirá o padrão de rotas `/api/v1/` e permitirá **criar**, **listar**, **buscar por ID**, **atualizar** e **remover** professores. Além disso, será adicionado um **middleware** para log de requisições.

---

### Pré-requisitos

- Docker: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Postman: [Download Postman](https://www.postman.com/downloads/)

### Endpoints da API:

- `POST /api/v1/professores/`: Cadastra um novo professor.
- `GET /api/v1/professores/`: Lista todos os professores.
- `GET /api/v1/professores/{professor_id}`: Busca um professor pelo ID.
- `PATCH /api/v1/professores/{professor_id}`: Atualiza dados de um professor.
- `DELETE /api/v1/professores/{professor_id}`: Remove um professor do sistema.
- `DELETE /api/v1/professores/`: Reseta a lista de professores.

---

### Código da API (FastAPI)

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()

professores = [
    {"id": 1, "nome": "Professor 1", "email": "professor_1@example.com", "sala_de_atendimento": "Sala 101"},
    {"id": 2, "nome": "Professor 2", "email": "professor_2@example.com", "sala_de_atendimento": "Sala 102"}
]

class ProfessorBase(BaseModel):
    nome: str
    email: str
    sala_de_atendimento: str

class Professor(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    sala_de_atendimento: str

class ProfessorAtualizar(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    sala_de_atendimento: Optional[str] = None


# Funções auxiliares
def gerar_id_unico():
    """
    Fun o para gerar um ID  único para cada professor.
    
    Caso a lista de professores esteja vazia, retorna 1.
    Caso contr rio, retorna o maior ID presente na lista de professores + 1.
    """
    if professores:
        return max(prof["id"] for prof in professores) + 1
    return 1

def buscar_professor_por_id(professor_id: int):
    """
    Busca um professor na lista de professores pelo seu ID.
    
    Se o professor for encontrado, retorna o dicionário com as informa es do professor.
    Caso contrário, retorna None.
    """
    for prof in professores:
        if prof["id"] == professor_id:
            return prof
    return None

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    inicio = time.time()
    response = await call_next(request)
    duracao = time.time() - inicio
    print(f"{request.method} {request.url.path} - {duracao:.4f}s")
    return response

@app.post("/api/v1/professores/", status_code=201)
def criar_professor(professor: ProfessorBase):
    for prof in professores:
        if prof["email"] == professor.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
    novo_professor = professor.dict()
    novo_professor["id"] = gerar_id_unico()
    # Adiciona o novo professor à lista de professores
    professores.append(novo_professor)
    return {"message": "Professor cadastrado com sucesso!", "professor": professor}

@app.get("/api/v1/professores/", response_model=List[Professor])
def listar_professores():
    return professores

@app.get("/api/v1/professores/{professor_id}")
def obter_professor(professor_id: int):
    for prof in professores:
        if prof["id"] == professor_id:
            return prof
    raise HTTPException(status_code=404, detail="Professor não encontrado.")

@app.patch("/api/v1/professores/{professor_id}")
def atualizar_professor(professor_id: int, dados: ProfessorAtualizar):
    professor = buscar_professor_por_id(professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado.")
    
    # Verifica se o email já existe para outro professor
    if dados.email:
        for prof in professores:
            if prof["email"] == dados.email and prof["id"] != professor_id:
                raise HTTPException(status_code=400, detail="Email já cadastrado.")

    # Atualiza os dados do professor
    if dados.nome is not None:
        professor["nome"] = dados.nome
    if dados.email is not None:
        professor["email"] = dados.email
    if dados.sala_de_atendimento is not None:
        professor["sala_de_atendimento"] = dados.sala_de_atendimento

    # Retorna o professor atualizado    
    return {"message": "Professor atualizado com sucesso!", "professor": professor}


@app.delete("/api/v1/professores/{professor_id}")
def remover_professor(professor_id: int):
    for prof in professores:
        if prof["id"] == professor_id:
            professores.remove(prof)
            return {"message": "Professor removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Professor não encontrado.")

# Reiniciar o dataset
@app.delete("/api/v1/professores/")
def limpar_professores():
    global professores
    professores = [
        {"id": 1, "nome": "Professor 1", "email": "professor_1@example.com", "sala_de_atendimento": "Sala 101"},
        {"id": 2, "nome": "Professor 2", "email": "professor_2@example.com", "sala_de_atendimento": "Sala 102"}
    ]
    return {"message": "Dataset limpo com sucesso!", "professores": professores}
```

### Explicação das Funcionalidades da API de Professores

1. **Adicionar Professor**:
   - O endpoint `POST /api/v1/professores/` cadastra um novo professor no sistema.
   - O corpo da requisição deve conter os campos `nome`, `email` e `sala_de_atendimento`.
   - Um `id` único é gerado automaticamente para cada professor cadastrado.

2. **Listar Professores**:
   - O endpoint `GET /api/v1/professores/` retorna uma lista com todos os professores cadastrados.
   - Caso não haja professores cadastrados, uma lista vazia é retornada.

3. **Buscar Professor por ID**:
   - O endpoint `GET /api/v1/professores/{professor_id}` permite buscar um professor específico pelo seu `ID`.
   - Caso o ID não exista, é retornado um erro 404 com a mensagem "Professor não encontrado".

4. **Atualizar Professor**: 
   - O endpoint `PATCH /api/v1/professores/{professor_id}` atualiza os dados de um professor existente.
   - Pode-se alterar qualquer campo (`nome`, `email`, `sala_de_atendimento`), mas o `ID` permanece inalterado.
   - Apenas os campos informados no corpo da requisição serão atualizados.

5. **Remover Professor**: 
   - O endpoint `DELETE /api/v1/professores/{professor_id}` remove um professor do sistema com base no seu `ID`.
   - Caso o professor não seja encontrado, é retornado um erro 404.

6. **Resetar Lista de Professores**:
   - O endpoint `DELETE /api/v1/professores/` reseta a lista de professores, removendo todos os registros.
   - Retorna uma mensagem de sucesso após a limpeza.

7. **Middleware de Logging (Bônus)**:
   - A API conta com um middleware que registra:
     - O método HTTP utilizado (ex: GET, POST, PATCH, DELETE)
     - O caminho do endpoint acessado
     - O tempo total de processamento da requisição
   - Esses logs são úteis para análise de performance e rastreamento de requisições.

---

### Executando a API

1. Instale as dependências:
```bash
pip install fastapi uvicorn
```

2. Execute:
```bash
uvicorn main:app --reload
```

3. Documentação disponível em:
```
http://127.0.0.1:8000/docs
```

---

### Docker

```yml
version: '3'
services:
  backend:
    build: ./backend
    restart: always
    ports:
      - "8000:8000"
```

---

### Exercício Proposto:

1. Implementar o CRUD completo do **seu gerenciador de alunos da pratica-1** usando FastAPI.
2. O CRUD deve conter as seguintes funcionalidades:
    - `POST /api/v1/alunos/`: Cadastra um novo aluno.
    - `GET /api/v1/alunos/`: Lista todos os alunos.
    - `GET /api/v1/alunos/{aluno_id}`: Busca um aluno pelo ID.
    - `PATCH /api/v1/alunos/{aluno_id}`: Atualiza dados de um aluno.
    - `DELETE /api/v1/alunos/{aluno_id}`: Remove um aluno do sistema.
    - `DELETE /api/v1/alunos/`: Reseta a lista de alunos.
3. Cada aluno deve possuir os seguintes atributos:
   - Nome
   - E-mail
   - Curso (GES, GEC) **Pelo menos 2 cursos**
   - Matrícula (gerada automaticamente com base no curso, ex: 1, 2, 3, etc.)
   - ID (curso + matrícula sequencial por curso, ex: GES1, GES2, GEC1, GEC2, etc.)
     - **OBS**: Se um aluno for deletado, o ID não pode ser reutilizado.
4. Executar a API usando docker-compose (**OBRIGATÓRIO**).
5. Criar uma **collection** no Postman usando os exemplos disponíveis em [Criando teste de API](postman/postman.md)
6. Os testes devem conter pelo menos adição de 3 alunos por curso, listagem de alunos, busca por ID, atualização de dados e remoção de alunos.
7. A Lógica de geração de ID será avaliada usando a collection do postman e o codigo da api.
8. Subir a **collection** na pasta `pratica-4a/api-tests`.
9. Tirar prints dos resultados e subir na pasta `pratica-4a/img`.

Prints:
- Summary dos resultados do postman
- Logs do container contendo as chamadas na API.

### Observação Importante

## ENTREGAR O PROJETO COM A MESMA ESTRUTURA!
```sh
 - aulas/
    - pratica-x/ # o x é o número da prática
       - api-tests/ # aqui vão os arquivos de testes do postman (collection e test run)
          - C216-L1-PRATICA-x-Nome_Matricula.postman_collection.json
       - img/ # aqui vão os prints solicitados
          - logs-api.png
          - postman.png
 - backend/ # o backend deve estar na raiz do repositório
    - main.py
    - Dockerfile
    - requirements.txt
docker-compose.yml
```
---

[Voltar ao início](../../README.md)