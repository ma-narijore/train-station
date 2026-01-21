import pytest

from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from depo.models import (
    Station,
    Route,
    Train,
    TrainType,
    Crew,
    Journey,
    Order,
    Ticket,
)

from depo.serializers import JourneySerializer

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def api_client(user):
    client = APIClient()

    # Generate token for the user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set JWT header
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def station(db):
    return Station.objects.create(
        name="Kyiv",
        latitude=39.91,
        longitude=-122.41,
    )


@pytest.fixture
def route(db, station):
    destination = Station.objects.create(
        name="Lviv",
        latitude=39.91,
        longitude=-122.41,
    )
    return Route.objects.create(source=station, destination=destination, distance=540)


@pytest.fixture
def train_type(db):
    return TrainType.objects.create(name="Intercity")


@pytest.fixture
def train(db, train_type):
    return Train.objects.create(
        name="Train1", cargo_num=5, places_in_cargo=10, train_type=train_type
    )


@pytest.fixture
def crew_member(db):
    return Crew.objects.create(first_name="John", last_name="Smith")


@pytest.fixture
def journey(db, route, train, crew_member):
    journey = Journey.objects.create(
        route=route,
        train=train,
        departure_time="2026-01-20T08:00:00Z",
        arrival_time="2026-01-20T12:00:00Z",
    )
    journey.crew.add(crew_member)
    return journey


@pytest.mark.django_db
def test_create_order_with_ticket(api_client, user, journey):
    url = reverse("order-list")  # DRF router: order-list

    payload = {"seat": 14, "cargo": 2, "journey_id": journey.id}

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

    data = response.json()
    assert "id" in data

    # Check that Ticket was created
    order = Order.objects.get(id=data["id"])
    ticket = order.tickets.first()
    assert ticket.seat == 14
    assert ticket.cargo == 2
    assert ticket.journey.id == journey.id


def test_create_order_with_ticket(api_client, user, journey):
    url = reverse("order-list")  # DRF router: order-list

    payload = {"seat": 14, "cargo": 2, "journey_id": journey.id}

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

    data = response.json()
    assert "id" in data

    # Check that Ticket was created
    order = Order.objects.get(id=data["id"])
    ticket = order.tickets.first()
    assert ticket.seat == 14
    assert ticket.cargo == 2
    assert ticket.journey.id == journey.id


@pytest.mark.django_db
def test_list_orders(api_client, user, journey):
    # api_client.force_authenticate(user=user)

    order = Order.objects.create(user=user)
    Ticket.objects.create(order=order, journey=journey, seat=1, cargo=1)

    url = reverse("order-list")
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == order.id


@pytest.mark.django_db
def test_retrieve_order_detail(api_client, user, journey):
    # api_client.force_authenticate(user=user)
    order = Order.objects.create(user=user)
    Ticket.objects.create(order=order, journey=journey, seat=10, cargo=1)

    url = reverse("order-detail", args=[order.id])
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert "tickets" in data
    assert data["tickets"][0]["seat"] == 10
    assert data["tickets"][0]["cargo"] == 1


@pytest.mark.django_db
def test_journey_serializer(api_client, journey):
    url = reverse("journey-detail", args=[journey.id])
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert "route" in data
    assert "train" in data
    assert "crew" in data
    assert data["crew"][0] == JourneySerializer(journey).data["crew"][0]


@pytest.mark.django_db
def test_route_list_serializer(api_client, route):
    url = reverse("route-list")
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()[0]
    assert data["view"] == "Kyiv-Lviv"
    assert data["distance"] == 540
