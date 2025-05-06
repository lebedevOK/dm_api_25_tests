def test_delete_v1_account_login(account_helper, prepare_user):
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)

    # Получаем две независимые сессии
    response1 = account_helper.user_login(login=login, password=password)
    token1 = {'X-Dm-Auth-Token': response1.headers['X-Dm-Auth-Token']}

    response2 = account_helper.user_login(login=login, password=password)
    token2 = {'X-Dm-Auth-Token': response2.headers['X-Dm-Auth-Token']}

    # Подтверждение, что это действительно два разных токена (сессии)
    assert token1 != token2, "Ожидались два разных токена для независимых сессий"

    # Удаляем текущую сессию (вторую)
    account_helper.dm_account_api.login_api.set_headers(token2)
    response = account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 204, f'Ожидался статус 204, получен {response.status_code}'

    # Проверяем: первая сессия должна работать
    account_helper.dm_account_api.account_api.set_headers(token1)
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, f'Первая сессия должна быть активной, статус: {response.status_code}'

    # Вторая — нет
    account_helper.dm_account_api.account_api.set_headers(token2)
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401, f'Вторая сессия должна быть удалена, статус: {response.status_code}'
