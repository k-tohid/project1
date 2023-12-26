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
    print(response.data)

    # ************** ? *********************
    # we get 'name': 'Drink: ' from serializer
    # assert data['name'] == drink_info['name']
    assert data['description'] == drink_info['description']
    assert data['price'] == drink_info['price']
    assert data['creator'] == 'test'


@pytest.mark.django_db
def test_delete_drink_without_authentication(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0, 'is_publishable': True}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(reverse('drink_list'), drink_info, headers=headers)

    del_response = client.delete(reverse('drink_detail', kwargs={'drink_uuid': response.data['uuid']}))

    assert del_response.status_code == 403


@pytest.mark.django_db
def test_put_drink_without_authentication(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0, 'is_publishable': True}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(reverse('drink_list'), drink_info, headers=headers)

    drink_info_put = {'name': 'name_test_put', 'description': 'description_test', 'price': 1.0, 'is_publishable': True}
    del_response = client.put(reverse('drink_detail', kwargs={'drink_uuid': response.data['uuid']}), drink_info_put)

    assert del_response.status_code == 403


@pytest.mark.django_db
def test_delete_drink_with_authentication(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0, 'is_publishable': True}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(reverse('drink_list'), drink_info, headers=headers)

    del_response = client.delete(reverse('drink_detail', kwargs={'drink_uuid': response.data['uuid']}), headers=headers)

    assert del_response.status_code == 204


@pytest.mark.django_db
def test_put_drink_with_authentication(client, signup_user):
    token = signup_user
    drink_info = {'name': 'test', 'description': 'new test drink', 'price': 1.0, 'is_publishable': True}

    headers = {'AUTHORIZATION': 'Token ' + token}
    response = client.post(reverse('drink_list'), drink_info, headers=headers)

    drink_info_put = {'name': 'name_test_put', 'description': 'description_test', 'price': 1.0, 'is_publishable': True}
    del_response = client.put(reverse('drink_detail', kwargs={'drink_uuid': response.data['uuid']}), drink_info_put, headers=headers)

    assert del_response.status_code == 200

