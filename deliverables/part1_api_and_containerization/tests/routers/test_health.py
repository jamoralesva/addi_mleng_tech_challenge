from datetime import datetime

import pytest


class TestHealthCheckRouter:

    def test_health_check_success(self, client):
        """
        Prueba que el endpoint /health responda correctamente.
        """
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "OK"
        assert data["version"] == "1.0.0"
        
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("El timestamp no tiene un formato ISO 8601 válido")