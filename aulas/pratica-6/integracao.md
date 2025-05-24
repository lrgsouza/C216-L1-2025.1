[Voltar ao início](../../README.md)
---

# Prática 6 - Integração dos sistemas distribuídos utilizando containers e docker-compose

## Objetivo

Integrar todos os componentes do sistema de gerenciamento de professores utilizando contêineres:

- Backend: FastAPI + PostgreSQL
- Frontend: Flask + Bootstrap
- Orquestração: Docker Compose

---

## Estrutura dos Serviços

```bash
.
├── backend/           # FastAPI + asyncpg
│   ├── db/
│   │   ├── init.sql
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/          # Flask com templates e Bootstrap
│   ├── app.py
│   ├── Dockerfile
│   ├── templates/
│   │   ├── _messages.html
│   │   ├── cadastro.html
│   │   ├── editar.html
│   │   ├── index.html
│   │   ├── navbar.html
│   │   └── professores.html
│   └── static/
│       └── styles.css
├── docker-compose.yaml
```

---

## Funcionalidades do Sistema

### Backend FastAPI

- CRUD completo de professores persistido em banco PostgreSQL
- Middleware de logging
- Reset do banco com SQL

### Frontend Flask

- Página inicial com boas-vindas
- Cadastro de novos professores (formulário)
- Listagem de professores com opções de editar/excluir
- Formulário de edição com valores preenchidos
- Botão para resetar o banco de dados

### Banco de Dados

- PostgreSQL com volume persistente e `init.sql` de carga inicial

---

## Como Executar

### 1. Construir e subir os serviços:

```bash
docker-compose up --build
```

### 2. Acessar os sistemas:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
- Banco de dados: `localhost:5432` (usuario: `postgres`, senha: `postgres`, db: `professores`)

---

## Observações

- O frontend Flask se comunica com o backend FastAPI utilizando requisições HTTP.
- A estilização foi feita com Bootstrap.
- A prática demonstra o uso de sistemas distribuídos com separação clara de camadas.

---

## Exercício Proposto

1. Adapte o sistema para gerenciar alunos, mantendo a mesma estrutura.
2. A lógica de matrícula deve ser mantida.
3. Execute o sistema e tire prints das telas. (PODE SER GRAVADO EM VIDEO)
    - Tela inicial
    - Tela de reset
    - Tela de cadastro
    - Tela de listagem
    - Tela de edição
    - Cadastre pelo menos 3 alunos
    - Edite pelo menos 1 aluno
    - Exclua pelo menos 1 aluno
    - Evidencie todas as operações realizadas com prints
    - Salve os logs gerados em um arquivo `logs.txt`
4. Salve os prints na pasta `pratica-6/img`. Ou envie um link para o video.
5. Salve os logs na pasta `pratica-6` em um arquivo `logs.txt`.

---
[Voltar ao início](../../README.md)