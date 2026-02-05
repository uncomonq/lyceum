# Lyceum

Первый проект на Django.

Проект запускается в dev-режиме, который предназначен только для разработки и

Проект запускается в dev-режиме, который предназначен только для разработки и
отличается повышенной отладочной информацией и пониженной безопасностью.

## Зависимости

Зависимости разделены по назначению:

- `requirements/prod.txt` — зависимости для запуска проекта;
- `requirements/test.txt` — зависимости для запуска тестов (включает `prod.txt`);
- `requirements/dev.txt` — зависимости для разработки (включает `test.txt`).

Для обратной совместимости файл `requirements.txt` ссылается на `prod.txt`.

## Развёртывание и запуск (Linux)

1. Клонировать репозиторий:
   ```bash
   git clone <repo_url>
   cd lyceum
   ```
2. Создать и активировать виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установить продовые зависимости:
   ```bash
   pip install -r requirements/prod.txt
   ```
4. Создать `lyceum/.env` файл для конфигурации (пример):
   ```bash
   cat > lyceum/.env << 'EOF_ENV'
   SECRET_KEY=django-insecure-dev-key
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   EOF_ENV
   ```
5. Перейти в директорию проекта с `manage.py`:
   ```bash
   cd lyceum
   cd lyceum
   ```
6. Применить миграции базы данных:
   ```bash
   python manage.py migrate
   ```
7. Запустить сервер разработки:
   ```bash
   python manage.py runserver
   ```

После запуска приложение будет доступно по адресу:
После запуска приложение будет доступно по адресу:

http://127.0.0.1:8000/

## Дополнительно

- Для запуска тестов установите также:
  ```bash
  pip install -r requirements/test.txt
  ```
- Для разработки (линтеры и прочие dev-инструменты):
  ```bash
  pip install -r requirements/dev.txt
  ```
