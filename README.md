# DM API Tests

_API test automation project for DM.

## Installation

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:_
```bash
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `tests/` - test cases
- `dm_api_account/` - API client methods
- `utilities/` - helper functions

## Running Tests

```bash
pytest tests/
```

## Generating Allure Report

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results