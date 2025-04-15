import requests
from requests import Response
from dm_api_account.models.registration import Registration

class AccountApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_v1_account(self, json: Registration) -> Response:
        """
        Register new user
        :param json: registration model
        :return: Response
        """
        response = requests.post(
            url=f'{self.base_url}/v1/account',
            json=json.model_dump(exclude_none=True)
        )
        return response