from rest_framework.generics import CreateAPIView

from users.serializer import UserRegisterSerializer


# Create your views here.

class UserRegister(CreateAPIView):
    serializer_class = UserRegisterSerializer
