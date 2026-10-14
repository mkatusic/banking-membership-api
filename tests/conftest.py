import os

import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app


test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    test_database_url = dotenv_values(".env.test").get("DATABASE_URL")

if not test_database_url:
    raise RuntimeError("Test database URL is not configured")

if not test_database_url.endswith("/banking_membership_test_db"):
    raise RuntimeError("Refusing to run tests against a non-test database")


test_engine = create_engine(test_database_url)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)