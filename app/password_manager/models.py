import uuid

from django.db import models
from django.conf import settings

from cryptography.fernet import Fernet


class ManagerPassword(models.Manager):
    fernet = Fernet(settings.SECRET_PASS_KEY)

    def get_de_password(self, *args, **kwargs):
        result_get = super().get(*args, **kwargs)
        result_get.password = self.fernet.decrypt(result_get.password).decode()
        return result_get

    def filter_de_password(self, *args, **kwargs):
        queryset = super().filter(*args, **kwargs)
        for obj in queryset:
            obj.password = self.fernet.decrypt(obj.password).decode()
        return queryset



class StoragePassword(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    password = models.CharField(max_length=128)
    service_name = models.CharField(max_length=255)

    objects = ManagerPassword()
