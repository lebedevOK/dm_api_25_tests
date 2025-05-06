def test_delete_v1_account_login_all(account_helper, prepare_user):
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email

    # Регистрация и активация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    token = {
        'X-Dm-Auth-Token': account_helper.dm_account_api.login_api.session.headers['X-Dm-Auth-Token']
    }
    # Удаляем все сессии пользователя
    account_helper.dm_account_api.login_api.set_headers(token)
    account_helper.dm_account_api.login_api.delete_v1_account_login_all()


