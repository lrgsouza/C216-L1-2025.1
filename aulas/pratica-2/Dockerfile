# Usando uma imagem base do Python
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo Python para o diretório de trabalho no container
COPY sistema_faculdade.py .

# Segundo exemplo, copiando todos os arquivos do diretório app para o diretório de trabalho no container
# COPY ./app .

# Comando para executar o script Python
CMD ["python", "sistema_faculdade.py"]