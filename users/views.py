from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

