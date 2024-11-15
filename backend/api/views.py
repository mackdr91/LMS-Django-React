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
from api import models as api_models
from .utils import generate_random_string
from decimal import Decimal


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


class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True) # Filter active categories
    serializer_class = api_serializers.CategorySerializer
    permission_classes = [AllowAny]


class CourseListAPIView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status="Published",
        teacher_course_status="Published"
    ) # Filter published courses
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """
        Retrieve a Course object based on the slug provided in the URL.

        This method fetches the course with the given slug from the database.
        If no course is found, it raises a DoesNotExist exception.

        :return: The Course instance corresponding to the slug.
        :raises: Course.DoesNotExist if no course with the slug exists.
        """
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(slug=slug, platform_status="Published", teacher_course_status="Published")
        return course



class CartAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartSerializer
    queryset = api_models.Cart.objects.all()
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        """
        Create a new cart.

        This method creates a new cart and returns it.

        :param request: The request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The created cart object.
        """
        course_id = request.data['course_id'] # Get the course ID from the request data
        user_id = request.data['user_id'] # Get the user ID from the request data
        country = request.data['country'] # Get the country from the request data
        price = request.data['price'] # Get the price from the request data
        cart_id = request.data['cart_id'] # Get the cart ID from the request data


        course = api_models.Course.objects.filter(id=course_id).first() # Get the course with the given ID
        """
        If the user ID is not "undefined", get the user with the given ID
        If the user ID is "undefined", set the user to None
        """
        if user_id != "undefined":
            user = CustomUser.objects.filter(id=user_id).first() # Get the user with the given ID
        else:
            user = None
        """
        If the country is not "undefined", get the country with the given name
        If the country is "undefined", set the country to "United States"
        """
        try:
            country_object = api_models.Country.objects.filter(name=country_name).first() # Get the country with the given name
            country = country_object.name
        except:
            country_object = None
            country = "United States"

        if country_object:
            tax_rate = country_object.tax_rate / 100 # Get the tax rate for the country
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first() # Get the cart with the given ID

        """
        If the cart already exists, update it
        If the cart does not exist, create a new one
        """

        if cart:
            cart.course = course
            cart.user = user
            cart.country = country
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee) # Calculate the total price
            cart.save()

            return Response({'message': 'Cart updated successfully'}, status=status.HTTP_201_CREATED)
        else:
            cart = api_models.Cart()
            cart.course = course
            cart.user = user
            cart.country = country
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee) # Calculate the total price
            cart.save()


            return Response({'message': 'Cart created successfully'}, status=status.HTTP_201_CREATED)





