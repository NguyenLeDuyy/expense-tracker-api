import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from fastapi.testclient import TestClient
from app.core.deps import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    token = response.json()["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_category(client, auth_headers):
    response = client.post("/categories/", json={
        "name": "Food",
        "monthly_budget": 1000000
    }, headers=auth_headers)
    return response.json()["data"]