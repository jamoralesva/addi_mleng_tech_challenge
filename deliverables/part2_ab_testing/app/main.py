from fastapi import FastAPI

from .api.v1.router import router

app = FastAPI(
    title="ML Experiment Lifecycle API",
    version="1.0.0",
    description="API for managing the lifecycle of machine learning experiments"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Experiment API"}

# Entry point para debugging local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1348)