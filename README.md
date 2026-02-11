# Lyceum

[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585/-/commits/main)

Первый проект на Django.

Проект запускается в dev-режиме, который предназначен только для разработки и
отличается повышенной отладочной информацией и пониженной безопасностью. 
Чтобы запусть проект в prod-режиме нужно создать .env с DEBUG=False, 
или же указать при запуске:
   ```
   DEBUG=False python3 manage.py runserver
   ```

При запуске значения настроек подтягиваются из файла `.env` (если он есть).

## Зависимости

Зависимости разделены по назначению:

- `requirements/prod.txt` — зависимости для запуска проекта;
- `requirements/test.txt` — зависимости для запуска тестов (включает `prod.txt`);
- `requirements/dev.txt` — зависимости для разработки (включает `test.txt`).

## CI/CD

В пайплайне настроены проверки:

- `flake8` с плагинами:
  - `pep8-naming` (проверка имён по PEP8);
  - `flake8-import-order` (порядок импортов);
  - `flake8-quotes` (проверка кавычек).
- `black --check` (проверка форматирования без изменения файлов).

## Развёртывание и запуск (Linux)

1. Клонировать репозиторий:
   ```bash
   git clone https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585
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
4. Перейти в директорию проекта с `manage.py`:
   ```bash
   cd lyceum
   ```
5. Выполните миграцию:
   ```
   python3 manage.py migrate
   ```
6. Запустить сервер разработки:
   ```bash
   python3 manage.py runserver
   ```

После запуска приложение будет доступно по адресу:

http://127.0.0.1:8000/

## Дополнительно

- Для запуска тестов установите также:
  ```bash
  pip install -r requirements/test.txt
  cd lyceum
  python3 manage.py test
  ```
- Для разработки (dev-инструменты):
  ```bash
  pip install -r requirements/dev.txt
  ```