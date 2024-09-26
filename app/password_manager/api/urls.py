from django.urls import path, re_path

from .views import PasswordListAPIView, PasswordRetrieveCreateAPIView


urlpatterns = [
    path('password/<str:service_name>/', PasswordRetrieveCreateAPIView.as_view()),
    re_path('password/(?:/(?P<service_name>\b))?$', PasswordListAPIView.as_view())
]