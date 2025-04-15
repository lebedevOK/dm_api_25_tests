# DM API Tests

Проект автоматизации тестирования API для DM.

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/lebedevOK/dm_api_25_tests.git
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
```

3. Активировать виртуальное окружение:
```bash
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

4. Установить зависимости:
```bash
pip install -r requirements.txt
```

## Структура проекта

- `tests/` - тесты
- `dm_api_account/` - методы работы с API
- `utilities/` - вспомогательные функции
- `configuration.py` - конфигурация проекта
- `conftest.py` - фикстуры pytest

## Запуск тестов

```bash
pytest tests/
```

## Генерация отчета Allure

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results