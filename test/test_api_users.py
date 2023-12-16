import pytest

# URLS -> users URL
USER_SIGNUP_URL = 'http://127.0.0.1:8000/users/signup'
USER_LOGIN_URL = 'http://127.0.0.1:8000/users/login'


@pytest.mark.django_db
def test_user_signup(client):
    user_info = {
        'username': 'test',
        'password': 'password'
    }

    response = client.post(USER_SIGNUP_URL, user_info)
    data = response.data

    assert response.status_code == 201
    assert 'token' in data
    assert 'user' in data
    assert 'password' not in data['user']
    assert data['user']['username'] == 'test'


@pytest.mark.django_db
def test_user_signup_incomplete_info(client):
    user_info = {
        'username': 'test'
    }

    response = client.post(USER_SIGNUP_URL, user_info)

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_login(client):
    user_info = {
        'username': 'test',
        'password': 'password'
    }

    # create user
    client.post(USER_SIGNUP_URL, user_info)
    # login user
    response = client.post(USER_LOGIN_URL, user_info)
    data = response.data

    assert response.status_code == 200
    assert 'token' in data
    assert 'user' in data
    assert 'password' not in data['user']
    assert data['user']['username'] == 'test'
