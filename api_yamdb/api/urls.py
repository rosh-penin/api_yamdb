from django.urls import path, include
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()
# router_v1.register(r'', CategoryViewSet)
# router_v1.register(r'', GenreViewSet)
# router_v1.register(r'', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
