# Dockerfile для FastAPI приложения
# Как запустить контейнер:
# docker build . -t app
# docker run -p 8080:8000 -it app

FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.6.1"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]