# Usando a imagem oficial do Python 3.9 slim
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt ./

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para dentro do contêiner
COPY . .

# Expor a porta 8000 para comunicação externa
EXPOSE 8000

# Comando para iniciar a API com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
