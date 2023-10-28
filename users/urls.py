from django.urls import path

from users.apps import UsersConfig
from users.views import UserListAPIView
app_name = UsersConfig.name


urlpatterns = [path('', UserListAPIView.as_view())
               ]