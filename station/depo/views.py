from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Station, Route, Train, TrainType, Crew, Journey, Order

from .serializers import (
    StationSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    RouteCreateSerializer,
    TrainSerializer,
    TrainCreateSerializer,
    TrainTypeSerializer,
    CrewListSerializer,
    CrewDetailSerializer,
    JourneySerializer,
    JourneyCreateSerializer,
    OrderWriteSerializer,
    OrderSerializer,
    OrderDetailSerializer,
)

from .permissions.permissions import StationPermission


# --------------------
# Station
# --------------------
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [StationPermission]


# --------------------
# Route
# --------------------
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    permission_classes = [StationPermission]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return RouteCreateSerializer
        return RouteDetailSerializer


# --------------------
# Train
# --------------------
class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    permission_classes = [StationPermission]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TrainCreateSerializer
        return TrainSerializer


# --------------------
# TrainType
# --------------------
class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = [StationPermission]


# --------------------
# Crew
# --------------------
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    permission_classes = [StationPermission]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CrewDetailSerializer
        return CrewListSerializer


# --------------------
# Journey
# --------------------
class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.select_related("route", "train").prefetch_related("crew")
    permission_classes = [StationPermission]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return JourneyCreateSerializer
        return JourneySerializer


# --------------------
# Order
# --------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related(
        "tickets__journey__crew",  # for TicketSerializer nested fields
        "tickets__journey__train",
        "tickets__journey__route",
    )
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return OrderWriteSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save()
