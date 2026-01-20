# 🚆 Train Station API

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-Active-red)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

A Django REST Framework project for managing train stations, routes, journeys, tickets, and orders.  
Includes JWT authentication (SimpleJWT) and PostgreSQL as the database.  

---

## Features

- CRUD operations for:
  - Stations
  - Routes
  - Trains & Train Types
  - Crew
  - Journeys
  - Orders & Tickets
- JWT Authentication using **SimpleJWT**
- Nested serializers for detailed API responses
- Dockerized development environment with PostgreSQL
- Fully tested using `pytest` and `pytest-django`

---

## Technologies

- Python 3.11
- Django 4.x
- Django REST Framework
- SimpleJWT
- PostgreSQL 15
- Docker & Docker Compose
- Pytest / Pytest-Django

---

## Project Structure

train-station/
├─ manage.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ myproject/
│  ├─ settings.py
│  └─ ...
├─ depo/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  └─ ...

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Git

### Clone the repository

```bash
git clone https://github.com/yourusername/train-station.git
cd train-station
```

Build and run Docker containers
```bash
docker-compose build
docker-compose up -d
```


web → Django app

db → PostgreSQL

Run migrations
```bash
docker-compose exec web python manage.py migrate
```

Create a superuser (optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

Access API

Django server: http://localhost:8000

Authentication (JWT)

Obtain a token:

POST /api/token/
{
  "username": "youruser",
  "password": "yourpassword"
}


Response:

{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}


Use the access token in headers:

Authorization: Bearer <access_token>

Running Tests
docker-compose exec web pytest


Uses pytest-django

api_client fixture automatically handles JWT authentication

API Endpoints
Resource	Endpoint	Methods
Stations	/api/stations/	GET, POST, PUT, DELETE
Routes	/api/routes/	GET, POST, PUT, DELETE
Trains	/api/trains/	GET, POST, PUT, DELETE
Train Types	/api/train-types/	GET, POST, PUT, DELETE
Crew	/api/crew/	GET, POST, PUT, DELETE
Journeys	/api/journeys/	GET, POST, PUT, DELETE
Orders	/api/orders/	GET, POST, PUT, DELETE
Tickets	/api/tickets/	GET, POST, PUT, DELETE
Docker Notes

Use docker-compose down -v to remove containers and volumes

PostgreSQL data is persisted via Docker volume (postgres_data)

Contributing

Fork the repository

Create a branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m "Add feature")

Push to the branch (git push origin feature/your-feature)

Open a Pull Request

License

MIT License © [Oleh]
