import requests


class LoginApi:
    def __init__(self, host, email):
        self.host = host
        self.email = email

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response