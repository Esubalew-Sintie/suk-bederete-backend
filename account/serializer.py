from rest_framework import serializers
from.models import Account
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use the custom user manager's create_user method to create a user
        user = User.objects.create_user(**validated_data)
        return user