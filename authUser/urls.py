
from unicodedata import name
from django.urls import path
from authUser.views import MyObtainTokenPairView, RegisterUserView,ChangePasswordView,UpdateProfileView, LogoutUserView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [ 

    # path("api/login", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("api/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register", RegisterUserView.as_view(), name="user_registeration"),
    path("api/changePassword/<int:pk>/", ChangePasswordView.as_view(), name="user_change_password" ),
    path("api/changeProfile/<int:pk>/", UpdateProfileView.as_view(), name="user_change_profile"),
    path("api/logout", LogoutUserView.as_view(), name="user_logout" )

    # path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all')

]


