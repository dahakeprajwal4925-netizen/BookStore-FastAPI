
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Create a separate temporary test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Database dependency for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test client fixture
@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Test 1: Create a new book
def test_create_book(client):
    response = client.post(
        "/api/v1/books/",
        json={
            "title": "Python Testing",
            "author": "Prajwal Dahake",
            "category": "Programming",
            "price": 499,
            "stock": 10
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Python Testing"


# Test 2: Get all books
def test_get_all_books(client):
    response = client.get("/api/v1/books/")

    assert response.status_code == 200
    assert response.json() == []


# Test 3: Get a book by ID
def test_get_book_by_id(client):
    create_response = client.post(
        "/api/v1/books/",
        json={
            "title": "FastAPI Basics",
            "author": "Prajwal Dahake",
            "category": "Programming",
            "price": 599,
            "stock": 5
        }
    )

    book_id = create_response.json()["id"]

    response = client.get(f"/api/v1/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "FastAPI Basics"

# Test 4: Update complete book using PUT
def test_update_book(client):
    create_response = client.post(
        "/api/v1/books/",
        json={
            "title": "Python Basics",
            "author": "Prajwal",
            "category": "Programming",
            "price": 499,
            "stock": 10
        }
    )

    book_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/books/{book_id}",
        json={
            "title": "Advanced Python",
            "author": "Prajwal",
            "category": "Programming",
            "price": 799,
            "stock": 15
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Python"


# Test 5: Update selected fields using PATCH
def test_partial_update_book(client):
    create_response = client.post(
        "/api/v1/books/",
        json={
            "title": "FastAPI Basics",
            "author": "Prajwal",
            "category": "Programming",
            "price": 499,
            "stock": 10
        }
    )

    book_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/books/{book_id}",
        json={"price": 899}
    )

    assert response.status_code == 200
    assert response.json()["price"] == 899
    assert response.json()["title"] == "FastAPI Basics"


# Test 6: Delete a book
def test_delete_book(client):
    create_response = client.post(
        "/api/v1/books/",
        json={
            "title": "Delete Me",
            "author": "Prajwal",
            "category": "Programming",
            "price": 299,
            "stock": 5
        }
    )

    book_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/books/{book_id}"
    )

    assert response.status_code == 200

    # Verify that the book no longer exists
    get_response = client.get(
        f"/api/v1/books/{book_id}"
    )

    assert get_response.status_code == 404
