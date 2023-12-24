import pytest

# URLS -> drink urls
DRINK_LIST_URL = 'http://127.0.0.1:8000/drinks/'
DRINK_DETAIL_URL = 'http://127.0.0.1:8000/drinks/'
DRINK_PRIVATE_DETAIL_URL = 'http://127.0.0.1:8000/private/drinks/'

# URLS -> users URL
USER_SIGNUP_URL = 'http://127.0.0.1:8000/users/signup'
USER_LOGIN_URL = 'http://127.0.0.1:8000/users/login'


@pytest.mark.django_db
def test_get_all_drinks(client, create_5_drink):
    response = client.get(DRINK_LIST_URL)

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_new_drink(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(DRINK_LIST_URL, drink_info, headers=headers)
    data = response.data

    assert data['name'] == 'test'
    assert data['description'] == 'new test drink'
    assert data['price'] == 1.0
    assert data['creator'] == 'test'
