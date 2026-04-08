from typing import List, Optional

from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

from source.application.graph import workflow
from source.application.state import GraphState


class ChatAgentResponse(BaseModel):
    response: str
    flow: List[str]
    selected_topic: Optional[str]
    selected_agent: Optional[str]
    reasoning: str
    current_step: int
    conversation_id: str

class ChatHistoryManager:
    """
    Simple in-memory chat history manager. En producción, esto debería ser reemplazado 
    por una solución persistente como Redis o una base de datos.
    """
    def __init__(self):
        self.history = {}

    def add_message(self, conversation_id: str, role: str, content: str):
        if conversation_id not in self.history:
            self.history[conversation_id] = []
        self.history[conversation_id].append({"role": role, "content": content})

    def get_history(self, conversation_id: str):
        return self.history.get(conversation_id, [])     
    

class ChatAgent:
    """
    ChatAgent encapsula la lógica de manejar preguntas de los usuarios, 
    interactuar con el workflow y gestionar el estado de la conversación.
    """
    def __init__(self, chat_history_manager: ChatHistoryManager):
        # Quizas en el futuro queramos agregar un checkpointer como dependencia externa
        self.checkpointer = MemorySaver()
        self.graph = workflow.compile(checkpointer=self.checkpointer)
        self.chat_history_manager = chat_history_manager

    async def respond(
            self, 
            user_id: str, 
            conversation_id: str, 
            question: str
        ) -> ChatAgentResponse:
        """
        Maneja una pregunta del usuario, actualiza el estado de la conversación y 
        devuelve la respuesta generada.
        """

        chat_history = self.chat_history_manager.get_history(conversation_id)

        state = GraphState(
            question=question.strip(),
            messages=chat_history,
            user_id=user_id,
            conversation_id=conversation_id,
            generation="",
            flow=[],
            user_data=None,
            user_data_summary=None,
            selected_topic=None,
            selected_agent=None,
        )
        
        config = {"configurable": {"thread_id": conversation_id}}
        result = await self.graph.ainvoke(input=state, config=config)

        self.chat_history_manager.add_message(conversation_id, "user", question)
        self.chat_history_manager.add_message(
            conversation_id, "assistant", result["generation"]
        )

        step = result.get("current_step")

        return ChatAgentResponse(
            response=result.get("generation", "(no response generated)"),
            flow=result.get("flow", []),
            selected_topic=result.get("selected_topic", "-"),
            selected_agent=result.get("selected_agent", "-"),
            reasoning=result.get("router_reasoning", ""),
            current_step=step if step else 0,
            conversation_id=conversation_id
        )
        

class ChatAgentFactory:
    """
    Factory para crear instancias de ChatAgent. 
    Esto permite centralizar la configuración y facilitar la inyección de dependencias.
    """
    def create(self) -> ChatAgent:
        if getattr(self, "_chat_agent", None) is None:
            self.chat_history_manager = ChatHistoryManager()
            self._chat_agent = ChatAgent(chat_history_manager=self.chat_history_manager)
        return self._chat_agent



       