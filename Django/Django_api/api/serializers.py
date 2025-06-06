from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Transforms the CustomUser model instances into JSON and
    handles user creation with password write-only for security.
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only and never returned in responses
        }

    def create(self, validated_data):
        """
        Create and return a new CustomUser instance,
        using the create_user method to properly hash the password.
        """
        return CustomUser.objects.create_user(**validated_data)