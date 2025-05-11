# Usando a Imagem do Python:
FROM python:3.13.2

# Definindo o Diretório de Trabalho:
WORKDIR /app

# Copiando os Códigos e Requerimentos do Servidor:
COPY . .

# Instalando as Dependências, Sem Usar Cache no "pip":
RUN pip install --no-cache-dir -r requirements.txt

# Expondo a Porta do Servidor:
EXPOSE 64223

# Executando a API do Servidor:
CMD ["python", "ServerTest.py"]
