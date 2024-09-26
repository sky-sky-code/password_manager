from cryptography.fernet import Fernet
from django.conf import settings
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from password_manager.models import StoragePassword
from .serializers import SerializerReadPassword, SerializerCreatePassword

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter


class PasswordRetrieveCreateAPIView(GenericAPIView):
    queryset = StoragePassword.objects.all()
    serializer_class = SerializerReadPassword

    @extend_schema(responses={200: SerializerReadPassword})
    def get(self, request, *args, **kwargs):
        try:
            obj = StoragePassword.objects.get_de_password(service_name=kwargs['service_name'])
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise Http404

    @extend_schema(request=SerializerCreatePassword, responses={201: SerializerCreatePassword})
    def post(self, request, *args, **kwargs):
        self.serializer_class = SerializerCreatePassword
        serializer = self.get_serializer(data=request.data | kwargs)
        serializer.is_valid(raise_exception=True)
        exists_service = StoragePassword.objects.filter(service_name=kwargs['service_name']).exists()

        fernet = Fernet(settings.SECRET_PASS_KEY)
        secret_password = fernet.encrypt(request.data['password'].encode()).decode('utf8')
        if exists_service:
            obj_pass = StoragePassword.objects.get(service_name=kwargs['service_name'])
            obj_pass.password = secret_password
            obj_pass.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        StoragePassword.objects.create(
            service_name=kwargs['service_name'],
            password=secret_password
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PasswordListAPIView(ListAPIView):
    queryset = StoragePassword.objects.all()
    serializer_class = SerializerReadPassword

    def get_queryset(self):
        if not self.request.query_params:
            pass
        self.queryset = StoragePassword.objects.filter_de_password(service_name__contains=self.request.query_params['service_name'])
        return self.queryset

    @extend_schema(parameters=[OpenApiParameter(name='service_name', type=str, required=False)])
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
