import pytest
from dm_api_account0.api import AccountApi
from configuration import config

@pytest.fixture
def account_api():
    return AccountApi(config.SERVICE_URL)