import json

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

class AccountHelper:
    def __init__(self, dm_account_api:DMApiAccount, mailhog:MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login:str, password:str, email:str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был зарегистрирован. Статус код ответа {response.status_code}'
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'
        token = self.get_activation_token_by_login(login=login, response=response)
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
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f'Пользователь не смог авторизоваться. Статус код ответа {response.status_code}'
        return response

    @staticmethod
    def get_activation_token_by_login(login, response):
        token = None
        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        return token


