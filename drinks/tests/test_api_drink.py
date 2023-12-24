import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_all_drinks(client, create_5_drink):
    response = client.get(reverse('drink_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_new_drink(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(reverse('drink_list'), drink_info, headers=headers)
    data = response.data

    assert data['name'] == 'test'
    assert data['description'] == 'new test drink'
    assert data['price'] == 1.0
    assert data['creator'] == 'test'
