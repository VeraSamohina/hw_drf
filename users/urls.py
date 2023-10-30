from django.urls import path

from users.apps import UsersConfig
from users.views import UserRetrieveAPIView
app_name = UsersConfig.name


urlpatterns = [path('<int:pk>/', UserRetrieveAPIView.as_view())
               ]