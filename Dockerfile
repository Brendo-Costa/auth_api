FROM python:3.8-slim-buster

#nome do diretório que conterá a aplicação
WORKDIR /auth_app

#
ENV PYTHONUNBUFFERED 1

#copia o arquivo da pasta atual "requirements.txt" copiado para um arquivo "requirements.txt" dentro do container
COPY requirements.txt requirements.txt

#roda, dentro do container, o comando para instalar todas as dependencias do projeto listadas no arquivo "requirements.txt"
RUN pip install -r requirements.txt

#copiando todos os arquivos desse diretório atual para um, dentro do container. 
COPY . .

#comando para subir o container
CMD ["python", "manage.py" , "runserver", "0.0.0.0:8000"]