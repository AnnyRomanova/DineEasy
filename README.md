<div id="header" align="left">
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWR2NGF1MmZ2Z3p0ZmxkZjA3emdtY2p1NWxmZWVibXFuaHVja2ljOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nnihjfnlmVeEFqXEy3/giphy.gif">
</div>

# DineEasy 🍽️ — API для управления бронированием столов

### :sparkles: Умный и элегантный бэкенд-сервис для автоматизации резервирования столов в ресторане.  
### :busts_in_silhouette: Подходит для администраторов и клиентов, чтобы быстро управлять посадкой гостей.

---

## :hammer_and_wrench: Технологии

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original-wordmark.svg" title="FastAPI" alt="FastAPI" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pytest/pytest-original-wordmark.svg" title="Pytest" alt="Pytest" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="PostgreSQL" alt="PostgreSQL" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" title="SQLAlchemy" alt="SQLAlchemy" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original-wordmark.svg" title="Git" alt="Git" width="40" height="40"/>
</div>

---

## 🚀 Установка и запуск

### 1. Установи зависимости
```bash
pip install -r requirements.txt
```

### 2. Создай .env файл в корне проекта

```
# ----------------------
#   Postgres
# ----------------------
POSTGRES_DB=DineEasyDB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# ----------------------
#   Приложение
# ----------------------
APP_NAME=Dine Easy
DB__HOST=localhost
DB__PORT=5432
DB__USER=postgres
DB__PASSWORD=postgres
DB__DB=DineEasyDB

# ----------------------
#   Режим запуска
# ----------------------
ENV_MODE=local
```
### 3. Запусти проект в Docker
```commandline
docker-compose build
docker-compose up -d
```
#### При запуске внутри Docker переменная ENV_MODE автоматически устанавливается в docker, чтобы использовать DB__HOST=db

### 4. Применение миграций
```commandline
alembic upgrade head
```
### 5. Запуск тестов
#### 💻 Локально:
```
pytest tests
```
#### Используется временная тестовая база, которая автоматически создаётся и удаляется на время сессии тестов. Все миграции применяются на лету.

## 🔁 Примеры данных для POST-запросов
### 📌 Создание стола (/tables/)
```json
{
  "name": "Table_1",
  "seats": 3,
  "location": "window"
}
```
### 📌 Бронирование стола (/reservations/)
```json
{
  "customer_name": "Oleg",
  "table_id": 1,
  "reservation_time": "2025-12-31T23:59:59+00:00",
  "duration_minutes": 120
}
```
## 📖 Документация Swagger
#### После запуска проекта можешь открыть:

👉 http://localhost:8000/docs

#### И использовать интерактивный UI для тестирования всех эндпоинтов.