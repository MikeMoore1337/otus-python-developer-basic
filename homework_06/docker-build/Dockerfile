# Dockerfile для FastAPI приложения
# Как запустить контейнер:
# docker build . -t app
# docker run -p 8080:8000 -it app

FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ../src ./

CMD ["flask", "run"]
