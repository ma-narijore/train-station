from rest_framework import serializers

from .models import Station, Route


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class RouteListSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            "view",
            "distance",
        )

    def get_view(self, obj):
        return f"{obj.source.name}-{obj.destination.name}"


class RouteDetailSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            "source",
            "destination",
            "distance",
        )

    def get_source(self, obj):
        return obj.source.name

    def get_destination(self, obj):
        return obj.destination.name