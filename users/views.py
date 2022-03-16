from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """Create new user in the system"""
    serializer_class = UserSerializer
