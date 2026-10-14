# Banking Membership API

A REST API for managing banking customers, membership plans, and subscriptions, built with Python, FastAPI, and PostgreSQL.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL, SQLAlchemy, Alembic
- **Testing:** pytest, HTTPX

## Features

- Customer creation and retrieval with email validation
- Membership plan management with configurable pricing
- Subscription creation and cancellation
- One active subscription per customer, enforced through a PostgreSQL partial unique index
- Subscription history preserved after cancellation
- Database migrations using Alembic
- Automated unit and integration tests using a separate PostgreSQL test database

**In progress:** Idempotent subscription creation using request hashing and PostgreSQL transactions.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/customers` | List customers |
| GET | `/customers/{customer_id}` | Get customer |
| POST | `/customers` | Create customer |
| GET | `/plans` | List plans |
| POST | `/plans` | Create plan |
| POST | `/subscriptions` | Create subscription |
| POST | `/subscriptions/{subscription_id}/cancel` | Cancel subscription |

Interactive API documentation is available at `/docs`.

## Project Structure

```text
app/
├── api/          # API routes
├── db/           # Database configuration
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
├── services/     # Business logic
└── main.py

migrations/       # Alembic migrations
tests/            # Unit and integration tests
```

## Getting Started

**Requirements:** Python and PostgreSQL.

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/mkatusic/banking-membership-api.git
cd banking-membership-api
python -m pip install -r requirements.txt
```

2. Create a PostgreSQL database named `banking_membership_db` and configure `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/banking_membership_db
```

3. Apply migrations and start the server:

```bash
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

## Testing

Tests use pytest and a separate PostgreSQL database (`banking_membership_test_db`).

Create `.env.test` with the test database connection string, apply the Alembic migrations to that database, then run:

```bash
python -m pytest -v
```

Integration tests use transaction rollback to keep test data isolated.

## Next Steps

- Complete idempotent subscription creation
- Implement membership upgrades and downgrades
- Expand integration and concurrency testing
- Add Docker and GitHub Actions CI