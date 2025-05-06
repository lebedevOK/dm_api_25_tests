
def test_delete_v1_account_login_all(account_helper, prepare_user):
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email

    # Регистрация и активация
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация: первая сессия
    account_helper.auth_client(login=login, password=password)
    token1 = {
        'X-Dm-Auth-Token': account_helper.dm_account_api.login_api.session.headers['X-Dm-Auth-Token']
    }

    # Авторизация: вторая сессия
    account_helper.auth_client(login=login, password=password)
    token2 = {
        'X-Dm-Auth-Token': account_helper.dm_account_api.login_api.session.headers['X-Dm-Auth-Token']
    }

    # Подтверждение, что это действительно два разных токена (сессии)
    assert token1 != token2, "Ожидались два разных токена для независимых сессий"

    # Удаление всех сессий с token2
    account_helper.dm_account_api.login_api.set_headers(token2)
    response = account_helper.dm_account_api.login_api.delete_v1_account_login_all()
    assert response.status_code == 204, f'Ожидался статус 204, получен {response.status_code}'

    # Обе сессии должны быть завершены
    account_helper.dm_account_api.account_api.set_headers(token1)
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401, f'Сессия token1 должна быть удалена, статус: {response.status_code}'

    account_helper.dm_account_api.account_api.set_headers(token2)
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401, f'Сессия token2 должна быть удалена, статус: {response.status_code}'

