from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StationViewSet,
    RouteViewSet,
    TrainViewSet,
    TrainTypeViewSet,
    CrewViewSet,
    JourneyViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register(r"station", StationViewSet)
router.register(r"route", RouteViewSet)
router.register(r"train", TrainViewSet)
router.register(r"train-type", TrainTypeViewSet)
router.register(r"crew", CrewViewSet)
router.register(r"journey", JourneyViewSet, basename="journey")
router.register(r"order", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
