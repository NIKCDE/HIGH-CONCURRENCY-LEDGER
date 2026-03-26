# Double Ledger High-Concurrency API

## Features
- Double-entry accounting system
- Atomic transactions
- Row-level locking
- Scalable service-layer architecture

## Tech Stack
- Django
- Django REST Framework
- PostgreSQL

## Endpoints
- POST /api/accounts/
- GET /api/accounts/
- POST /api/transactions/

## Run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

ARCHITECTURE BREAKDOWN (IMPORTANT FOR YOU):
Layer	-Responsibility
Models	-Data structure
Serializers	-Validation
Views (CBV)	-Request handling
Services	-Business logic
DB	-Concurrency safety