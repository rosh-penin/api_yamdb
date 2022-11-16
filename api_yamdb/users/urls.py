from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, UsersSignUp, UsersTokenObtain

app_name = 'users'


router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', UsersTokenObtain.as_view(), name='token_obtain'),
    path('v1/auth/signup/', UsersSignUp.as_view(), name='signup'),
    path('v1/', include(router_v1.urls))
]
