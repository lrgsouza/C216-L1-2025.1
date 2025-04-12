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