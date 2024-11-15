from rest_framework import serializers
from userauth.models import CustomUser, Profile
from api import models as api_models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import (
    validate_password,
)  # For password validation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod  #
    def get_token(cls, user):
        """
        Overwrites the method from the parent class to include custom claims in the JWT token.

        :param user: The user instance to generate the token for.
        :return: The JWT token with custom claims.
        """
        token = super().get_token(user)
        # Add custom claims
        token["full_name"] = user.full_name
        token["email"] = user.email
        token["username"] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    # Define custom password validation
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "password", "password2"]

    def validate(self, attrs):
        """
        Validate that the password fields match.

        :param attrs: The validated data.
        :raises serializers.ValidationError: If the password fields do not match.
        :return: The validated data.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.

        :param validated_data: The validated data.
        :return: The created user instance.
        """
        user = CustomUser.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username

        user.set_password(validated_data["password"])
        user.save()

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Category
        fields = [
            "title",
            "slug",
            "image",
            "course_count",
        ]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Teacher
        fields = [
            "user",
            "image",
            "full_name",
            "bio",
            "facebook",
            "linkedin",
            "twitter",
            "about",
            "country",
            "created_at",
            "updated_at",
            "students",
            "courses",
            "reviews",
        ]


class VariantItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.VariantItem
        fields = "__all__"


class VariantSerializer(serializers.ModelSerializer):
    variant_item = VariantItemSerializer()

    class Meta:
        model = api_models.Variant
        fields = "__all__"


class QuestionAnswerMessageSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Question_Answer_Message
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    messages = QuestionAnswerMessageSerializer(many=True)
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Question_Answer
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Cart
        fields = "__all__"


class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.CartOrderItem
        fields = "__all__"


class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer(many=True)

    class Meta:
        model = api_models.CartOrder
        fields = "__all__"


class Certificate(serializers.ModelSerializer):
    class Meta:
        model = api_models.Certificate
        fields = "__all__"


class CompletedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.CompletedCourse
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Note
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Review
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Notification
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Coupon
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Wishlist
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Country
        fields = "__all__"


class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only=True)
    completedLessons = CompletedCourseSerializer(many=True, read_only=True)
    curriculum = VariantItemSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = QuestionAnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = api_models.EnrolledCourse
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    students = EnrolledCourseSerializer(
        many=True
    )  # array that contains all the enrolled students
    curriculum = VariantItemSerializer(
        many=True
    )  # array that contains all the curriculum items
    lectures = VariantItemSerializer(
        many=True
    )  # array that contains all the lecture items

    class Meta:
        model = api_models.Course
        fields = [
            "teacher",
            "category",
            "title",
            "image",
            "slug",
            "file",
            "description",
            "created_at",
            "updated_at",
            "price",
            "language",
            "level",
            "platform_status",
            "teacher_course_status",
            "featured",
            "course_id",
            "date",
            "students",
            "curriculum",
            "lectures",
            "reviews",
        ]
