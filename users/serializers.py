from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """Serializer for user model"""
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "role", "password")

    def create(self, validated_data):
        """Create a new user"""
        return get_user_model().objects.create_user(**validated_data)
