import json
import time
from retrying import retry
from email.header import decode_header
import re
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Попытка номер {count+1}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('Превышено количество попыток получения токена.')
            if token:
                return token
            time.sleep(1)
        return None
    return wrapper

def decode_mime_header(value: str) -> str:
    parts = decode_header(value)
    decoded = ''
    for part, encoding in parts:
        decoded += part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
    return decoded


class AccountHelper:
    def __init__(self, dm_account_api:DMApiAccount, mailhog:MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login:str, password:str):
        response = self.dm_account_api.login_api.post_v1_account_login(json_data={'login': login, 'password': password})
        token = {
            'X-Dm-Auth-Token': response.headers.get('X-Dm-Auth-Token')}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        assert response.json()['resource']['login'] == login

    def register_new_user(self, login:str, password:str, email:str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был зарегистрирован. Статус код ответа {response.status_code}'
        # response = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'
        token = self.get_activation_token_by_login(login=login)
        assert token, f'Не найдено письмо для логина {login}. Статус код ответа {response.status_code}'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f'Пользователь не был активирован. Статус код ответа {response.status_code}'
        return response

    def user_login(self, login:str, password:str, remember_me=True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data={'login': login, 'password': password, 'rememberMe': remember_me})
        assert response.status_code == 200, f'Пользователь не смог авторизоваться. Статус код ответа {response.status_code}'
        return response

    def change_password(self, login: str, email: str, new_password: str):
        """
        Смена пароля пользователя по сбросу через email
        """
        # Шаг 1: запрос на сброс пароля
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code in [200, 201], f'Сброс пароля не инициирован. Статус код: {response.status_code}'

        # Шаг 2: получаем токен из письма
        token = self.get_token_by_change_password(login)
        if not token:
            return None

        # Шаг 3: меняем пароль
        change_data = {
            'login': login,
            'token': token,
            'oldPassword': None,
            'newPassword': new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=change_data)
        if response.status_code != 200:
            return None

        return True

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self,login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        return token



    @retry(stop_max_attempt_number=5, wait_fixed=1500, retry_on_result=lambda x: x is None)
    def get_token_by_change_password(self, login: str):
        """
        Извлечение токена сброса пароля из письма, отправленного Mailhog'ом
        """
        response = self.mailhog.mailhog_api.get_api_v2_messages(limit=15)
        assert response.status_code == 200, f'Не удалось получить письма. Статус код: {response.status_code}'

        for item in response.json()['items']:
            raw_subject = item['Content']['Headers'].get('Subject', [''])[0]
            subject = decode_mime_header(raw_subject)

            if 'Подтверждение сброса пароля' in subject and login in subject:
                body = item['Content']['Body']
                match = re.search(r'/password/([a-f0-9\-]{36})', body)
                if match:
                    return match.group(1)

        return None


