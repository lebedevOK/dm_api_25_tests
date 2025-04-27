from random import randint
import time
import json
import os

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utilities.helpers import Helpers
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

import structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_put_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)
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










