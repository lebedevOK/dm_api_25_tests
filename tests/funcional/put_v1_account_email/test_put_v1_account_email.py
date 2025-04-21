from random import randint
import time
import json
import os

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utilities.helpers import Helpers


def test_put_v1_account_email():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051', email='email')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = f'al{randint(1, 9999)}'
    password = '123456789'
    email = f"{login}@qw.ru"
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    response = account_api.post_v1_account(json_data=json_data)
    print(f'Register new user: {response.status_code}')
    assert response.status_code == 201, f'Пользователь не был зарегистрирован. Статус код ответа {response.status_code}'

    # Ждем 3 секунды
    time.sleep(3)

    # Получаем список писем
    response = mailhog_api.get_api_v2_messages()
    print(f'Get list of emails: {response.status_code}')
    assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'
    print(response.json())

    # Ищем письмо с нашим логином и получаем токен
    helpers = Helpers()
    token = helpers.get_activation_token_by_login(login, response)
    print(f'Get activation token: {response.status_code}')
    assert token, f'Не найдено письмо для логина {login}. Статус код ответа {response.status_code}'
    print(f'Activation token: {token}')

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(f'Activate registered user: {response.status_code}')
    assert response.status_code == 200, f'Пользователь не был активирован. Статус код ответа {response.status_code}'

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    print(f'Authenticate via credentials: {response.status_code}')
    assert response.status_code == 200, f'Пользователь не смог авторизоваться. Статус код ответа {response.status_code}'
    print(email)
    print(password)

    # Изменение email
    local_part = f'al{randint(1, 9999)}'
    email = f"{local_part}@qw.ru"
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    print(f'Change email: {response.status_code}')
    assert response.status_code == 200, f'Пользователь не смог изменить email. Статус код ответа {response.status_code}'
    print(email)
    print(password)

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    print(f'Authenticate via credentials: {response.status_code}')
    assert response.status_code == 403, f'Ожижаемый статус код - 403. Статус код ответа {response.status_code}'

    # Идем повторно в почту и получаем список писем
    response = mailhog_api.get_api_v2_messages()
    print(f'Get 2nd list of emails: {response.status_code}')
    assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'
    print(response.json())

    # Ищем письмо с нашим логином и получаем токен
    helpers = Helpers()
    token = helpers.get_activation_token_by_login(login, response)
    print(f'Get 2nd activation token: {response.status_code}')
    assert token, f'Не найдено письмо для логина {login}. Статус код ответа {response.status_code}'
    print(f'Activation token: {token}')

    # Активация изменненного пользователя
    response = account_api.put_v1_account_token(token=token)
    print(f'Activate changed user: {response.status_code}')
    assert response.status_code == 200, f'Пользователь не был активирован. Статус код ответа {response.status_code}'

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    print(f'Authenticate via credentials: {response.status_code}')
    assert response.status_code == 200, f'Пользователь не смог авторизоваться. Статус код ответа {response.status_code}'
    print(email)
    print(password)








