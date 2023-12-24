import pytest
from django.urls import reverse

from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def signup_user(client):
    user_info = {
        'username': 'test',
        'password': 'password'
    }

    response = client.post(reverse('user_signup'), user_info)
    data = response.data

    return data['token']


@pytest.fixture
def create_new_drink(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0}

    headers = {'AUTHORIZATION': 'Token ' + token}
    client.post(reverse('drink_list'), drink_info, headers=headers)

    return token


@pytest.fixture
def create_5_drink(client, signup_user):
    token = signup_user
    drink_info = [{'name': 'test', 'description': 'new test drink', 'price': 1.0},
                  {'name': 'test2', 'description': 'new test drink2', 'price': 2.0},
                  {'name': 'test3', 'description': 'new test drink3', 'price': 3.0},
                  {'name': 'test4', 'description': 'new test drink4', 'price': 4.0},
                  {'name': 'test5', 'description': 'new test drink5', 'price': 5.0}, ]

    headers = {'AUTHORIZATION': 'Token ' + token}

    for drink in drink_info:
        client.post(reverse('drink_list'), drink, headers=headers)

    return token
