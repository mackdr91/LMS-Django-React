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
            country_object = api_models.Country.objects.filter(name=country).first() # Get the country with the given name
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


class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serializers.CartSerializer
    queryset = api_models.Cart.objects.all()
    permission_classes = [AllowAny]


    def get_queryset(self): # Override the get_queryset method to filter the queryset
        """
        Override the get_queryset method to filter the queryset based on the cart_id parameter.

        :param self: The instance of the class
        :param cart_id: The cart_id parameter passed from the url
        :return: The filtered queryset
        """
        # a dictionary that contains the keyword arguments
        # that were passed to the view or serializer
        cart_id = self.kwargs['cart_id'] # Get the cart_id from the url
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset



class CartItemDeleteAPIView(generics.DestroyAPIView):

    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self): # Override the get_object method get a single object
        """
        Return a Cart object with the given cart_id and item_id.

        This method filters the queryset of Cart objects based on the cart_id and item_id
        parameters passed from the url and returns the first result.

        :param self: The instance of the class
        :param cart_id: The cart_id parameter passed from the url
        :param item_id: The item_id parameter passed from the url
        :return: The Cart object with the given cart_id and item_id
        """
        cart_id = self.kwargs['cart_id'] # Get the cart_id from the url
        item_id = self.kwargs['item_id'] # Get the item_id from the url
        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first() # Get the cart with the given cart_id and item_id=item_id)



class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id' # Set the lookup field to 'cart_id'

    def get_queryset(self): # Override the get_queryset method to filter the queryset
        """
        Override the get_queryset method to filter the queryset based on the cart_id parameter.

        :param self: The instance of the class
        :param cart_id: The cart_id parameter passed from the url
        :return: The filtered queryset
        """
        # a dictionary that contains the keyword arguments
        # that were passed to the view or serializer
        cart_id = self.kwargs['cart_id'] # Get the cart_id from the url
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Retrieve and return the total price, tax, and main total for all cart items.

        This method calculates the cumulative price, tax, and main total for all items
        in the cart associated with the specified cart ID. It retrieves the cart items
        from the database, computes the totals, and returns them in a response.

        :param request: The request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A response object containing the total price, tax, and main total.
        :rtype: Response
        """
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_main = 0.00

        # Calculate the total price, tax, and main total
        # for all items in the cart
        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_main += round(float(self.calculate_main_total(cart_item)), 2)


        data = {
                'price': total_price,
                'tax': total_tax,
                'total': total_main
            }

        return Response(data, status=status.HTTP_200_OK)


    def calculate_price(self, cart_item):
        """
        Calculate the price of a single item in the cart.

        This method takes a Cart object as an argument and returns
        the price of the item in the cart. The price is retrieved from
        the Cart object.

        :param self: The instance of the class
        :param cart_item: The Cart object
        :return: The price of the item in the cart
        :rtype: float
        """
        return cart_item.price

    def calculate_tax(self, cart_item):

        """
        Calculate the tax of a single item in the cart.

        This method takes a Cart object as an argument and returns
        the tax of the item in the cart. The tax is retrieved from
        the Cart object.

        :param self: The instance of the class
        :param cart_item: The Cart object
        :return: The tax of the item in the cart
        :rtype: float
        """
        return cart_item.tax_fee

    def calculate_main_total(self, cart_item):
        """
        Calculate the main total of a single item in the cart.

        This method takes a Cart object as an argument and returns
        the main total of the item in the cart. The main total is
        the price of the item in the cart.

        :param self: The instance of the class
        :param cart_item: The Cart object
        :return: The main total of the item in the cart
        :rtype: float
        """
        return cart_item.total


class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()


    def create(self, request, *args, **kwargs):
        full_name = request.data['full_name'] # Get the full name from the request data
        email = request.data['email'] # Get the email from the request data
        country = request.data['country'] # Get the country from the request data
        cart_id = request.data['cart_id'] # Get the cart ID from the request data
        user_id = request.data['user_id'] # Get the user ID from the request data

        if user_id != 0:
            user = CustomUser.objects.get(id=user_id)
        else:
            user = None

        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial = Decimal(0.00)
        total_main = Decimal(0.00)


        order = api_models.CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
        )

        for c in cart_items:
            api_models.CartOrderItem.objects.create(
                order=order,
                course=c.course,
                price=c.price,
                tax_fee=c.tax_fee,
                total=c.total,
                initial_total=c.total,
                teacher=c.course.teacher

            )

            total_price += Decimal(c.price)
            total_tax += Decimal(c.tax_fee)
            total_initial += Decimal(c.total)
            total_main += Decimal(c.total)

            order.teacher.add(c.course.teacher)

        order.subtotal = total_price
        order.tax_fee = total_tax
        order.initial_total = total_initial
        order.total = total_main
        order.save()

        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class CheckoutAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()
    lookup_field = 'order_id'


class CouponApplyAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CouponSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        order_id = request.data['order_id'] # Get the order ID from the request data
        code = request.data['code'] # Get the code from the request data

        order = api_models.CartOrder.objects.get(order_id=order_id)
        coupon = api_models.Coupon.objects.get(code=code)

        if coupon:
            order_items = api_models.CartOrderItem.objects.filter(order=order, teacher=coupon.teacher)
            for o in order_items:
                if coupon not in o.coupons.all():
                    discount = o.total * coupon.discount / 100

                    o.total -= discount
                    o.price -= discount
                    o.saved += discount
                    o.applied_coupon = True
                    o.coupons.add(coupon)

                    order.coupons.add(coupon)
                    order.total -= discount
                    order.subtotal -= discount
                    order.saved += discount

                    o.save()
                    order.save()
                    coupon.used_by.add(order.student)

                    return Response({'message': 'Coupon Found and Activated'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Coupon already applied'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)




