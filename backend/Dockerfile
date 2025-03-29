# Usando uma imagem base do Python
FROM python:3.10-slim

# Copiando requirements.txt para o container
COPY requirements.txt .

# Instalando dependências
RUN pip install -r requirements.txt
# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o código para o container
COPY main.py .

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]