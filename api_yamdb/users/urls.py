from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, SignUpViewSet

app_name = 'users'


router_v1 = routers.DefaultRouter()
router_v1.register(r'auth/signup', SignUpViewSet)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
