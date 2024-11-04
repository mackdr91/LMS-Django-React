#from django.shortcuts import render
from api import serializer as api_serializers
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.conf import settings

from userauth.models import CustomUser
from .utils import generate_random_string


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = (
        api_serializers.MyTokenObtainPairSerializer
    )  # Use custom serializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = api_serializers.RegisterSerializer
    permission_classes = [AllowAny]


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.CustomUserSerializer

    def get_object(self):

        """
        Retrieve a CustomUser object based on an email provided in the URL.

        This method fetches the first user matching the given email. If a user
        is found, a new OTP is generated and saved, a refresh token is created
        and stored, and a password reset link is printed to the console.

        :return: The CustomUser instance corresponding to the email, or None if no user is found.
        """
        email = self.kwargs['email'] # Get the email from the URL

        user = CustomUser.objects.filter(email=email).first() # Get the first user with the given email

        if user:

            uuidb64 = user.pk # Get the UUID of the user
            refresh = RefreshToken.for_user(user) # Generate a refresh token
            refresh_token = str(refresh.access_token) # Convert the refresh token to a string
            user.refresh_token = refresh_token # Save the refresh token to the user

            user.otp = generate_random_string() # Generate a new OTP
            user.save()


            link = f'http://localhost:5173/create-new-password/?otp={user.otp}&uuid={uuidb64}&refresh_token={refresh_token}'

            # Send an email with the password reset link
            merge_data = {
                'link': link,
                'username': user.username
            }



            subject = 'Password Reset Link'
            text_content = render_to_string('email/password_reset.txt', merge_data)
            html_content = render_to_string('email/password_reset.html', merge_data)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.EMAIL,
                to=[user.email],
                body=text_content
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            print(link)
            print(settings.EMAIL)


        return user


class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.CustomUserSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new password for a user.

        This method takes the OTP, UUID and new password from the request and
        updates the user's password.

        :param request: The request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A response object with a message indicating the password
            was changed successfully.
        """
        payload = request.data # Get the payload from the request
        otp = payload['otp'] # Get the OTP from the payload
        uuidb64 = payload['uuidb64'] # Get the UUID from the payload
        password = payload['password'] # Get the password from the payload

        user = CustomUser.objects.get(id=uuidb64, otp=otp) # Get the user with the given UUID and OTP

        # Update the user's password
        if user:
            user.set_password(password)
            user.otp = None
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)