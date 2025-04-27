import json
import random
import string

class Helpers:
    def __init__(self):
        pass
    
    def get_activation_token_by_login(self, login, response):
        token = None
        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        return token





# def random_string(length: int = 8) -> str:
#     """Generate random string of specified length"""
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
#
#
# def random_email() -> str:
#     """Generate random email"""
#     return f"{random_string()}@{random_string(6)}.com"