import pytest
from fastapi.testclient import TestClient

from deliverables.part1_api_and_containerization.app.main import app


@pytest.fixture(scope="module")
def client():
    """
    Fixture que provee un cliente de pruebas para FastAPI.
    """
    with TestClient(app) as c:
        yield c