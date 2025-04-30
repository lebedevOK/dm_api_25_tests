from random import randint
import time
import json
import os

from helpers.account_helper import AccountHelper
# from dm_api_account.apis.account_api import AccountApi
# from dm_api_account.apis.login_api import LoginApi
# from api_mailhog.apis.mailhog_api import MailhogApi
# from utilities.helpers import Helpers
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)
def test_post_v1_account_login():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = f'al{randint(1, 9999)}'
    password = '123456789'
    email = f"{login}@qw.ru"
    account_helper.register_new_user(login=login, password=password, email=email)

    # json_data = {
    #     'login': login,
    #     'email': email,
    #     'password': password
    # }
    # response = account.account_api.post_v1_account(json_data=json_data)
    # assert response.status_code == 201, f'Пользователь не был зарегистрирован. Статус код ответа {response.status_code}'
    #
    # # Ждем 3 секунды
    # time.sleep(3)
    #
    # # Получаем список писем
    # response = mailhog.mailhog_api.get_api_v2_messages()
    # assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'
    #
    # # Ищем письмо с нашим логином и получаем токен
    # helpers = Helpers()
    # token = helpers.get_activation_token_by_login(login, response)
    # assert token, f'Не найдено письмо для логина {login}. Статус код ответа {response.status_code}'
    #
    # # Активация пользователя
    # response = account.account_api.put_v1_account_token(token=token)
    # assert response.status_code == 200, f'Пользователь не был активирован. Статус код ответа {response.status_code}'

    account_helper.user_login(login=login, password=password)
    # # Авторизация пользователя
    # json_data = {
    #     'login': login,
    #     'password': password,
    #     'rememberMe': True
    # }
    # response = account.login_api.post_v1_account_login(json_data=json_data)
    # assert response.status_code == 200, f'Пользователь не смог авторизоваться. Статус код ответа {response.status_code}'











