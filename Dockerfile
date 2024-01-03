# Используйте официальный образ Python
FROM python:3.8-buster

# Установка переменных среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание и установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY piplist.txt /app/

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r piplist.txt

# Копирование файлов проекта в рабочую директорию
COPY . /app/

# Запуск команды приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
