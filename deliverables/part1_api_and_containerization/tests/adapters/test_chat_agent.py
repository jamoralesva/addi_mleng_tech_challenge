from unittest.mock import AsyncMock, MagicMock

import pytest

from deliverables.part1_api_and_containerization.app.adapters.chat_agent import (
    ChatAgent,
    ChatAgentResponse,
)


class TestChatAgent:
    """Pruebas para el ChatAgent."""

    @pytest.fixture
    def mock_history_manager(self):
        """Mock de la persistencia del historial."""
        manager = MagicMock()
        manager.get_history.return_value = []
        return manager

    @pytest.fixture
    def agent(self, mock_history_manager):
        """Instancia del agente con dependencias mockeadas."""
        agent = ChatAgent(chat_history_manager=mock_history_manager)
        agent.graph = AsyncMock()
        return agent

    @pytest.mark.asyncio
    async def test_respond_happy_path(self, agent, mock_history_manager):
        # Arrange
        user_id = "user_1"
        conv_id = "conv_1"
        question = "¿Cómo funciona el crédito?"
        
        # Ni idea del contenido exacto.
        graph_output = {
            "generation": "El crédito es un préstamo...",
            "flow": [],
            "selected_topic": "-",
            "selected_agent": "-",
            "router_reasoning": "El usuario pregunta por créditos.",
            "current_step": 2
        }
        agent.graph.ainvoke.return_value = graph_output

        # Act
        response = await agent.respond(user_id, conv_id, question)

        # Assert
        assert isinstance(response, ChatAgentResponse)
        assert response.response == "El crédito es un préstamo..."
        assert response.conversation_id == conv_id
        assert response.current_step == 2

        mock_history_manager.get_history.assert_called_once_with(conv_id)
        
        assert mock_history_manager.add_message.call_count == 2
        mock_history_manager.add_message.assert_any_call(
            conv_id, 
            "user", 
            "¿Cómo funciona el crédito?"
        )
        mock_history_manager.add_message.assert_any_call(
            conv_id, 
            "assistant", 
            "El crédito es un préstamo..."
        )

        called_state = agent.graph.ainvoke.call_args[1]["input"]
        assert called_state["question"] == "¿Cómo funciona el crédito?"
        assert called_state["user_id"] == user_id