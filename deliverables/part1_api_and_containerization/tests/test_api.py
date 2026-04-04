from datetime import datetime

import pytest


def test_health_check_success(client):
    """
    Prueba que el endpoint /health responda correctamente.
    """
    # 1. Ejecución
    response = client.get("/health")
    
    # 2. Validaciones de HTTP
    assert response.status_code == 200
    
    # 3. Validaciones de Contenido (Lógica)
    data = response.json()
    assert data["status"] == "OK"
    assert data["version"] == "1.0.0"
    
    # 4. Validación de Formato (Data Integrity)
    # Verificamos que el timestamp sea un string ISO válido
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("El timestamp no tiene un formato ISO 8601 válido")