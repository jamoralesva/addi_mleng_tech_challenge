
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..adapters.chat_agent import ChatAgentFactory, ChatAgentResponse

chat_agent = ChatAgentFactory().create()

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

class ChatRequest(BaseModel):
    question: str
    user_id: str
    conversation_id: str


@router.post(
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
    response: ChatAgentResponse = await chat_agent.respond(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        question=request.question
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump_json()
    )

    