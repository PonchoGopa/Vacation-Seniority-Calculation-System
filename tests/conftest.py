import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

from app.models import company, employee, vacation_policy, vacation_calculation
from app.models import vacation_policy_rule, vacation_request

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Fuerza una sola conexión compartida
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def company(client):
    response = client.post("/companies/", json={
        "name": "Test Company",
        "bonus_percentage": 0.25
    })
    return response.json()


@pytest.fixture
def policy(client, company):
    response = client.post("/policies/", json={
        "company_id": company["id"],
        "name": "Política Estándar",
        "rules": [
            {"years_required": 1, "vacation_days": 12},
            {"years_required": 2, "vacation_days": 14},
            {"years_required": 3, "vacation_days": 16},
            {"years_required": 4, "vacation_days": 18},
            {"years_required": 5, "vacation_days": 20},
            {"years_required": 6, "vacation_days": 22},
            {"years_required": 11, "vacation_days": 24},
            {"years_required": 16, "vacation_days": 26},
            {"years_required": 21, "vacation_days": 28},
            {"years_required": 26, "vacation_days": 30}
        ]
    })
    return response.json()


@pytest.fixture
def employee(client, company, policy):
    response = client.post("/employees/", json={
        "name": "Juan Pérez",
        "hire_date": "2022-01-01",
        "daily_salary": 500.0,
        "company_id": company["id"],
        "vacation_policy_id": policy["id"]
    })
    return response.json()