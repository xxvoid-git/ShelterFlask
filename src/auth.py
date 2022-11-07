from functools import wraps
from flask import request, Response
from src.adapters.repository import AccountRepository
from src import config


def auth_decorator(roles: list = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*argc, **kwargs):
            if request.authorization is None:
                return Response(status=401)
            login = request.authorization.get('username')
            password = request.authorization.get('password')

            account_repo = AccountRepository(config.get_connection())
            account = account_repo.get_by_login_pass(login, password)

            if account is not None and account.role in roles:
                return func(*argc, **kwargs)

            return Response(status=401)

        return wrapper
    return decorator


