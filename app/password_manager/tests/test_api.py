import urllib.parse

import pytest

from django.urls import reverse

from password_manager.models import StoragePassword


@pytest.mark.django_db
def test_post_create(db, api_client):
    url = reverse('password_rcu', kwargs={'service_name': 'yundex'})

    response = api_client.post(url, {'password': 'secret_pass'}, format='json')

    assert response.status_code == 201
    assert response.data['password'] == 'secret_pass'

    obj_pass = StoragePassword.objects.get_de_password(service_name='yundex')

    assert response.data['password'] == obj_pass.password


@pytest.mark.django_db
def test_post_update(db, api_client, passwords):
    url = reverse('password_rcu', kwargs={'service_name': 'Wink'})

    old_wink_password = StoragePassword.objects.get_de_password(service_name='Wink')

    assert old_wink_password.service_name == 'Wink'
    assert old_wink_password.password == 'secret_wink'

    response = api_client.post(url, {'password': 'new_secret_wink'}, format='json')

    assert response.status_code == 201
    assert response.data['password'] == 'new_secret_wink'

    update_obj_wink = StoragePassword.objects.get_de_password(service_name='Wink')

    assert update_obj_wink.password == 'new_secret_wink'


@pytest.mark.django_db
def test_get_password(db, api_client, passwords):
    url = reverse('password_rcu', kwargs={'service_name': 'Wink'})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == {'service_name': 'Wink', 'password': 'secret_wink'}


@pytest.mark.django_db
def test_get_part_service(db, api_client, passwords):
    url = reverse('password_list',) + "?" + urllib.parse.urlencode({'service_name': 'Wink'})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == [
            {'service_name': 'Wink', 'password': 'secret_wink'},
            {'service_name': 'WinkSpr', 'password': 'secret_wink_spr'}
        ]
