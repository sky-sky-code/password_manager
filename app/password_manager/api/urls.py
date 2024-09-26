from django.urls import path, re_path

from .views import PasswordListAPIView, PasswordRetrieveCreateAPIView


urlpatterns = [
    # rcu - retrieve, create, update
    path('password/<str:service_name>/', PasswordRetrieveCreateAPIView.as_view(), name='password_rcu'),
    re_path('password/(?:/(?P<service_name>\b))?$', PasswordListAPIView.as_view(), name='password_list')
]