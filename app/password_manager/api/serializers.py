from password_manager.models import StoragePassword
from rest_framework.serializers import ModelSerializer, CharField


class SerializerCreatePassword(ModelSerializer):
    class Meta:
        model = StoragePassword
        fields = ('password',)


class SerializerReadPassword(ModelSerializer):
    class Meta:
        model = StoragePassword
        fields = ('password', 'service_name')
