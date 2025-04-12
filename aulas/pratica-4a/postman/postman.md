## Criando uma Postman Collection para a API de Professores

### Passos Iniciais

1. **Abra o Postman** e clique em **New > Collection**.
2. Nomeie a coleção como `C216-L1-PRATICA-4a-NOME_MATRICULA`.
3. Abaixo temos exemplos de requisições para a API de professores.

---

### **GET - Listar todos os professores**
- **URL:** `http://localhost:8000/api/v1/professores/`
- **Testes:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
pm.test("Deve retornar uma lista", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});
```

---

### **POST - Criar novo professor**
- **URL:** `http://localhost:8000/api/v1/professores/`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "nome": "João da Silva",
  "email": "joao@inatel.br",
  "sala_de_atendimento": "B204"
}
```
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});
pm.test("Mensagem de sucesso", function () {
    pm.expect(pm.response.json().message).to.eql("Professor cadastrado com sucesso!");
});
```
---

### **GET - Buscar professor por ID**
- **URL:** `http://localhost:8000/api/v1/professores/3`
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
pm.test("Deve conter dados do professor", function () {
    pm.expect(pm.response.json()).to.have.property('nome');
});
```

---

### **PATCH - Atualizar dados de um professor**
- **URL:** `http://localhost:8000/api/v1/professores/3`
- **Body:**
```json
{
  "email": "joao.novo@joao@inatel.br"
}
```
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
pm.test("Mensagem de atualização", function () {
    pm.expect(pm.response.json().message).to.eql("Professor atualizado com sucesso!");
});
```

---

### **DELETE - Remover professor**
- **URL:** `http://localhost:8000/api/v1/professores/3`
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
pm.test("Mensagem de remoção", function () {
    pm.expect(pm.response.json().message).to.eql("Professor removido com sucesso!");
});
```

---

### 6. **DELETE - Resetar repositorio de professores**
- **URL:** `http://localhost:8000/api/v1/professores/`
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```
---

[Voltar](../crud-middleware-1.md)