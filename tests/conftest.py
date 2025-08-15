import pytest
import helpers.generator_user
from helpers.api_requests import create_user, get_auth_token, delete_user


@pytest.fixture
def data_for_user():
    return {
        "email": helpers.generator_user.email_generator(),
        "password": str(helpers.generator_user.password_generator()),
        "name": helpers.generator_user.name_generator()
    }

@pytest.fixture
def for_reg_delete_user(data_for_user):
    yield data_for_user
    token = get_auth_token(data_for_user["email"], data_for_user["password"])
    if token:
        delete_user(token)

@pytest.fixture
def for_auth_delete_user(data_for_user):
    create_user(data_for_user)
    yield data_for_user
    token = get_auth_token(data_for_user["email"], data_for_user["password"])
    if token:
        delete_user(token)