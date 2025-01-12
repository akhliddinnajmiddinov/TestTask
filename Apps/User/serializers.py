from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser 
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password')

    def validate_password(self, value):
        """
        validate the password weakness.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = CustomUser (
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user