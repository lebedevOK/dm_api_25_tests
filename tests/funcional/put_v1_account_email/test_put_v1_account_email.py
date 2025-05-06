def test_put_v1_account_email(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Изменение email
    new_email = f"{login}_new@qw.ru"
    json_data = {
        'login': login,
        'email': new_email,
        'password': password
    }
    # response = account_helper.dm_account_api.put_v1_account_email(json_data=json_data)
    response = account_helper.dm_account_api.account_api.put_v1_account_email(json_data=json_data)

    assert response.status_code == 200, f'Пользователь не смог изменить email. Статус код ответа {response.status_code}'

    # Неуспешная авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    # response = account_helper.login_api.post_v1_account_login(json_data=json_data)
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 403, f'Ожижаемый статус код - 403. Статус код ответа {response.status_code}'

    # Идем повторно в почту и получаем список писем
    # response = account_helper.mailhog.get_api_v2_messages()
    response = account_helper.mailhog.mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, f'Не удалось получить список писем. Статус код ответа {response.status_code}'

    # Ищем письмо с нашим логином и получаем токен
    token = account_helper.get_activation_token_by_login(login)
    assert token, f'Не найдено письмо для логина {login}. Статус код ответа {response.status_code}'

    # Активация изменненного пользователя
    # response = account.account_api.put_v1_account_token(token=token)
    response = account_helper.dm_account_api.account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, f'Пользователь не был активирован. Статус код ответа {response.status_code}'

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)



