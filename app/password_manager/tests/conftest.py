import pytest
from cryptography.fernet import Fernet

from rest_framework.test import APIClient
from django.conf import settings

from password_manager.models import StoragePassword


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def passwords():
    fernet = Fernet(settings.SECRET_PASS_KEY)
    secret_pass_wink = fernet.encrypt('secret_wink'.encode()).decode('utf8')
    secret_pass_wink_spr = fernet.encrypt('secret_wink_spr'.encode()).decode('utf8')
    secret_pass_google = fernet.encrypt('secret_google'.encode()).decode('utf8')

    StoragePassword.objects.create(
        service_name='Wink',
        password=secret_pass_wink
    )
    StoragePassword.objects.create(
        service_name='WinkSpr',
        password=secret_pass_wink_spr
    )

    StoragePassword.objects.create(
        service_name='Google',
        password=secret_pass_google
    )
