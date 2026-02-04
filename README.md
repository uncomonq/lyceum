# Lyceum

Первый проект на Django.
Запуск осуществляется в dev-режиме, который предназначен только для разработки и
отличается повышенной отладочной информацией и пониженной безопасностью.

## Запуск в dev-режиме (Linux)

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
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Применить миграции базы данных:
   ```bash
   python manage.py migrate
   ```
5. Запустить сервер разработки:
   ```bash
   python manage.py runserver
   ```

### После запуска приложение будет доступно по адресу:

http://127.0.0.1:8000/

> > > > > > > 81262e4 (Initial Django project structure)
