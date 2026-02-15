# Учебный проект «Lyceum»

[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585/-/commits/main)
## CI/CD

В пайплайне настроены проверки:

- `flake8 --verbose` с плагинами:
  - `pep8-naming` (проверка имён по PEP8);
  - `flake8-import-order` (порядок импортов);
  - `flake8-quotes` (проверка кавычек).
- `black --check` (проверка форматирования без изменения файлов).

Это учебный проект для Специализации Яндекс Лицея «Веб-разработка на Django

## Требования

- [Python](https://www.python.org/downloads/) (3.10, 3.11, 3.12, 3.13, 3.14)
- [Venv](https://pandac.in/blogs/venv-python/#:~:text=Install%20Python%203%20and%20venv,package%20you%20want%20to%20install.) (для создания виртульного окружения на Linux)
- [Git](https://git-scm.com/install/) (для клонирования репозитория)

## Зависимости

Зависимости разделены по назначению:

- `requirements/prod.txt` — зависимости для запуска проекта;
- `requirements/test.txt` — зависимости для запуска тестов (включает `prod.txt`);
- `requirements/dev.txt` — зависимости для разработки (включает `test.txt`).



## Устновка и запуск в dev-режиме (Linux)

1. Клонировать репозиторий:
   ```bash
   git clone https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585
   cd 379829-rizaeffk-course-1585
   ```
2. Создать и активировать виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установить dev зависимости:
   ```bash
   pip install -r requirements/dev.txt
   ```
4. Перейти в директорию проекта с `manage.py`:
   ```bash
   cd lyceum
   ```
5. Создание .env (проект содержит .env.example с дефолтными значениями переменных окружения, при необходимости отредактировать):
   ```bash
   cp .env.example .env
   ```
6. Выполните миграцию:
   ```
   python3 manage.py migrate
   ```
7. Запустить сервер разработки:
   ```bash
   python3 manage.py runserver
   ```

## Устновка и запуск в dev-режиме (Windows)

1. Клонировать репозиторий:
   ```powershell
   git clone https://gitlab.crja72.ru/django/2026/spring/course/students/379829-rizaeffk-course-1585
   cd 379829-rizaeffk-course-1585
   ```
2. Создать и активировать виртуальное окружение:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  
   ```
3. Установить dev зависимости:
   ```powershell
   pip install -r requirements/dev.txt
   ```
4. Перейти в директорию проекта с `manage.py`:
   ```powershell
   cd lyceum
   ```
5. Создание .env (проект содержит .env.example с дефолтными значениями переменных окружения, при необходимости отредактировать):
   ```powershell
   copy .env.example .env
   ```
6. Выполните миграцию:
   ```powershell
   python3 manage.py migrate
   ```
7. Запустить сервер разработки:
   ```powershell
   python3 manage.py runserver
   ```

После запуска приложение будет доступно по адресу:

http://127.0.0.1:8000/

## Дополнительно

- Для запуска тестов перейдите в корневую директорию и установите также:
  ```bash
  pip install -r requirements/test.txt
  cd lyceum
  python3 manage.py test
  ```
- Для запуска в prod-режиме так же перейдите в корневую директорию:
  ```bash
  pip install -r requirements/prod.txt
  cd lyceum
  python3 manage.py runserver
  ```