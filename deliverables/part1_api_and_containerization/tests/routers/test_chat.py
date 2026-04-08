import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from deliverables.part1_api_and_containerization.app.adapters.chat_agent import (
    ChatAgent,
    ChatAgentResponse,
)


class TestChatRouter:
    
    @pytest.fixture
    def mock_response(self):
        """Genera una respuesta predefinida para el agente."""
        return ChatAgentResponse(
            response="Hola Nicolas Mora, Esto es un mock",
            flow=[],
            selected_topic="-",
            selected_agent="-",
            reasoning="Respuesta mockeada para pruebas",
            current_step=1,
            conversation_id="conv456"
        )
    
    @pytest.fixture
    def mock_history_manager(self):
        """Mock de la persistencia del historial."""
        manager = MagicMock()
        manager.get_history.return_value = [] # Historial vacío por defecto
        return manager
    
    @pytest.fixture
    def mock_agent(self, mock_history_manager):
        """Instancia del agente con dependencias mockeadas."""
        agent = ChatAgent(chat_history_manager=mock_history_manager)
        # Mockeamos el grafo que se creó en el __init__
        agent.graph = AsyncMock()
        return agent

    @patch("deliverables.part1_api_and_containerization.app.routers.chat.chat_agent") 
    @pytest.mark.asyncio
    async def test_post_chat_success(self, mock_agent, mock_response, client):
        # Arrange
        mock_agent.respond = AsyncMock(return_value=mock_response)
        
        payload = {
            "question": "Hola, ¿quién eres?",
            "user_id": "user123",
            "conversation_id": "conv456"
        }

        # Act
        response = client.post("/chat", json=payload)

        # Assert
        assert response.status_code == 200

        response_json = json.loads(response.json())
        assert (
            response_json["response"] == "Hola Nicolas Mora, Esto es un mock"
        )
        mock_agent.respond.assert_called_once_with(
            user_id="user123",
            conversation_id="conv456",
            question="Hola, ¿quién eres?"
        )