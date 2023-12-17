# Базовый образ для сборки
FROM python:3.11

# Установка рабочей директории
WORKDIR /app

# Обновление pip
RUN pip install --upgrade pip

# Копирование зависимостей
COPY requirements.txt requirements.txt

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование приложения
COPY . .

# Установка Gunicorn
RUN pip install gunicorn

# CMD для Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]