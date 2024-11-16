from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # Core Endpoints
    path('course/category/', api_views.CategoryListAPIView.as_view(), name='course_category'),
    path('course/course-list/', api_views.CourseListAPIView.as_view(), name='course_list'),
    path('course/course-detail/<slug>/', api_views.CourseDetailAPIView.as_view(), name='course_detail'),
    path('course/cart/', api_views.CartAPIView.as_view(), name='course_create'),
    path('course/cart-list/<cart_id>/', api_views.CartListAPIView.as_view(), name='cart_list'),
    path('course/cart-item-delete/<cart_id>/<item_id>/', api_views.CartItemDeleteAPIView.as_view(), name='cart_item_delete'),
    path('cart/stats/<cart_id>/', api_views.CartStatsAPIView.as_view(), name='cart_stats'),


    # Authentication Endpoints
    path('user/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path ('user/register/', api_views.RegisterView.as_view(), name='user_register'),
    path ('user/password-reset-email/<email>/', api_views.PasswordResetEmailVerifyAPIView.as_view(), name='password_reset_email_verify'),
    path ('user/password-change/', api_views.PasswordChangeAPIView.as_view(), name='password_change'),
    path('order/create-order/', api_views.CreateOrderAPIView.as_view(), name='order_create/'),
    path('order/checkout/<order_id>/', api_views.CheckoutAPIView.as_view(), name='order_checkout/'),
    path('order/coupon-apply/', api_views.CouponApplyAPIView.as_view(), name='coupon_apply/'),
]

# ENDPOINTS

# http://127.0.0.1:8001/api/v1/user/token/
# http://127.0.0.1:8001/api/v1/user/token/refresh get a new access token
# http://127.0.0.1:8001/api/v1/user/register
# http://127.0.0.1:8001/api/v1/user/password-reset-email/<email>/
# http://127.0.0.1:8001/api/v1/user/password-change/

# http://127.0.0.1:8001/course/category/
# http://127.0.0.1:8001/course/course-list/
# http://127.0.0.1:8001/course/course-detail/<slug>/
# http://127.0.0.1:8001/course/cart/