# Используем официальный образ Python в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Выводим содержимое директории /app для проверки
RUN ls -la /app

# Открываем порт 8000 для доступа к Django приложению
EXPOSE 8000

# Запускаем Django приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]