from rest_framework import serializers

from .models import (
    Station,
    Route,
    Train,
    TrainType,
    Crew,
    Journey,
    Ticket,
    Order,
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


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


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = (
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
        )

    def get_train_type(self, obj):
        return obj.train_type.name


class TrainCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class CrewListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Crew
        fields = (
            "id",
            "full_name",
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class CrewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class CrewNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class JourneySerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    train = serializers.SerializerMethodField()
    crew = CrewNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew")

    def get_route(self, obj):
        return f"{obj.route.source.name}-{obj.route.destination.name}"

    def get_train(self, obj):
        return {
            "Name": obj.train.name,
            "Type": obj.train.train_type.name,
        }

    def get_crew(self, obj):
        return [f"{member.first_name} {member.last_name}" for member in obj.crew.all()]


class JourneyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    journey = serializers.SerializerMethodField()
    train = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "train",
            "seat",
            "cargo",
            "journey",
        )

    def get_journey(self, obj):
        return {
            "Destination": f"{obj.journey.route.source.name}--{obj.journey.route.destination.name}",
            "Departure": obj.journey.departure_time,
            "Crew": [
                f"{member.first_name} {member.last_name}"
                for member in obj.journey.crew.all()
            ],
        }

    def get_train(self, obj):
        return obj.journey.train.name


class TicketWriteSerializer(serializers.ModelSerializer):
    journey_id = serializers.PrimaryKeyRelatedField(
        queryset=Journey.objects.all(), source="journey"
    )
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source="order"
    )

    class Meta:
        model = Ticket
        fields = (
            "seat",
            "cargo",
            "journey_id",
            "order_id",
        )


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "user",
        )


class OrderWriteSerializer(serializers.ModelSerializer):
    seat = serializers.IntegerField(write_only=True)
    cargo = serializers.IntegerField(write_only=True)
    journey_id = serializers.PrimaryKeyRelatedField(
        queryset=Journey.objects.all(), source="journey", write_only=True
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "seat",
            "cargo",
            "journey_id",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        seat = validated_data.pop("seat")
        cargo = validated_data.pop("cargo")
        journey = validated_data.pop("journey")

        order = Order.objects.create(user=user)

        Ticket.objects.create(
            order=order,
            journey=journey,
            seat=seat,
            cargo=cargo,
        )

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "user",
            "tickets",
        )
