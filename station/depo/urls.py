from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StationViewSet, RouteViewSet,
)


router = DefaultRouter()
router.register(r'station', StationViewSet)
router.register(r'route', RouteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
