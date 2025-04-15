import requests
from random import randint


def test_post_v1_account():
    # Подготовка данных
    login = f'al{randint(1, 999)}'
    password = '123456789'
    email = f"{login}@qw.ru"
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    
    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )
    
    # Проверка ответа
    assert response.status_code == 201, f'Статус код ответа должен быть 201, но получен {response.status_code}'


def test_post_v1_account_empty_login():
    # Подготовка данных с пустым логином
    json_data = {
        'login': '',
        'email': 'test@test.ru',
        'password': '123456789'
    }
    
    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )
    
    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Login is required'


def test_post_v1_account_empty_email():
    # Подготовка данных с пустым email
    json_data = {
        'login': f'al{randint(1, 999)}',
        'email': '',
        'password': '123456789'
    }
    
    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )
    
    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Email is required'


def test_post_v1_account_empty_password():
    # Подготовка данных с пустым паролем
    json_data = {
        'login': f'al{randint(1, 999)}',
        'email': 'test@test.ru',
        'password': ''
    }
    
    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )
    
    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Password is required'
