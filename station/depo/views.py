from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Station, Route
from .serializers import (
    StationSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)
from .permissions.permissions import StationPermission

# Create your views here.
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [StationPermission]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    permission_classes = [StationPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer
        return RouteDetailSerializer
