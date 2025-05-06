def test_get_v1_account_auth(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация
    account_helper.auth_client(login=login, password=password)

    # Получение данных
    account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)

    # Сброс авторизации — убираем заголовок токена
    account_helper.dm_account_api.account_api.set_headers({})

    # Запрос без токена
    response = account_helper.dm_account_api.account_api.get_v1_account()

    # Проверка ошибки авторизации
    assert response.status_code == 401, f':Для неавторизованного пользователя ожидался статус 401, получен {response.status_code}'

