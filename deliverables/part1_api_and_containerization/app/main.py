from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, status
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

from source.application.graph import workflow
from source.application.state import GraphState

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
chat_history = []

app = FastAPI(
    title="ML Ops Challenge API",
    description="Servicio de inferencia basado en LangGraph",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    question: str
    user_id: str
    conversation_id: str

class ChatResponse(BaseModel):
    response: str
    flow: List[str]
    selected_topic: Optional[str]
    selected_agent: Optional[str]
    reasoning: str
    current_step: int
    conversation_id: str

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

@app.get(
    "/health",
    tags=["system"],
    summary="Check health of the service",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK
)
async def get_health():
    """
    Endpoint para monitoreo y Liveness/Readiness probes.
    """
    return HealthCheck(
        status="OK",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@app.post(
    "/chat",
    tags=["chat"],
    summary="Handle a user question and return a response",
    status_code=status.HTTP_200_OK
)
async def post_chat(request: ChatRequest):
    """
    Endpoint principal para manejar preguntas de los usuarios.
    Recibe un JSON con la pregunta, user_id y conversation_id, 
    y devuelve la respuesta generada.
    """
    state = GraphState(
        question=request.question.strip(), # TODO: hacer validaciones más robustas
        messages=chat_history,
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        generation="",
        flow=[],
        user_data=None,
        user_data_summary=None,
        selected_topic=None,
        selected_agent=None,
    )
    config = {"configurable": {"thread_id": request.conversation_id}}
    result = await graph.ainvoke(input=state, config=config)
    chat_history.append({"role": "user", "content": request.question})
    chat_history.append({"role": "assistant", "content": result["generation"]})

    step = result.get("current_step")

    return ChatResponse(
        response=result.get("generation", "(no response generated)"),
        flow=result.get("flow", []),
        selected_topic=result.get("selected_topic", "-"),
        selected_agent=result.get("selected_agent", "-"),
        reasoning=result.get("router_reasoning", ""),
        current_step=step if step else 0,
        conversation_id=request.conversation_id
    )

# Entry point para debugging local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)