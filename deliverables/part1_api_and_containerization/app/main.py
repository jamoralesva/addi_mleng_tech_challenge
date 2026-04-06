

from fastapi import FastAPI

from .routers import chat, health

app = FastAPI(
    title="ML Ops Challenge API",
    description="Servicio de inferencia basado en LangGraph",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(chat.router)

# Entry point para debugging local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)