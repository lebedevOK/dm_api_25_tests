def test_put_v1_account_password(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация со старым паролем
    account_helper.user_login(login=login, password=password)

    # Новый пароль
    new_password = '987654321'

    # Смена пароля через токен из письма
    account_helper.change_password(login=login, email=email, new_password=new_password)

    # Попытка входа со старым паролем — должна быть неудачной
    response = account_helper.dm_account_api.login_api.post_v1_account_login(
        json_data={'login': login, 'password': password}
    )
    assert response.status_code == 400, f'Ожидался 400 при входе со старым паролем, получен {response.status_code}'

    # Успешный вход с новым паролем
    account_helper.user_login(login=login, password=new_password)
