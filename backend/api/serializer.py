from rest_framework import serializers
from userauth.models import CustomUser, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password # For password validation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod #
    def get_token(cls, user):
        """
        Overwrites the method from the parent class to include custom claims in the JWT token.

        :param user: The user instance to generate the token for.
        :return: The JWT token with custom claims.
        """
        token = super().get_token(user)
        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token

class RegisterSerializer(serializers.ModelSerializer):
    # Define custom password validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attrs):
        """
        Validate that the password fields match.

        :param attrs: The validated data.
        :raises serializers.ValidationError: If the password fields do not match.
        :return: The validated data.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.

        :param validated_data: The validated data.
        :return: The created user instance.
        """
        user = CustomUser.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )

        email_username, _ = user.email.split('@')
        user.username = email_username

        user.set_password(validated_data['password'])
        user.save()
        
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

