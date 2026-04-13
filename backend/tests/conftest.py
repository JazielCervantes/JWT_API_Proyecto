"""
Configuración de pytest.
Define fixtures y setup global para tests.
"""
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Cambiar a BD de test antes de importar app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from app.database import Base, get_db


# Engine de test (SQLite en memoria)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Fixture que proporciona una sesión de BD para cada test.
    Crea y limpia la BD antes y después.
    """
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Fixture que proporciona cliente de test de FastAPI.
    """
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Fixture con datos de usuario de ejemplo."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_admin_data():
    """Fixture con datos de admin de ejemplo."""
    return {
        "email": "admin@example.com",
        "username": "adminuser",
        "password": "AdminPass123!",
        "full_name": "Admin User"
    }
