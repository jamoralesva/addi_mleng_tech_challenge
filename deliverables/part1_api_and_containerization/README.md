# Part 1 — API, Containerization & CI/CD

Place your deliverables for Part 1 here.

## Expected Files

- Your FastAPI application code
- `Dockerfile` — Production-ready Docker image
- `docker-compose.yml` — Multi-service setup (if applicable)
- CI/CD pipeline configuration (e.g., `.github/workflows/ci.yml`)
- Test files (unit, integration, API)
- This `README.md` — Update with your build/run instructions

## How to Run

*Important:* For this component to function correctly, the container image of the experiments service from part 2 must be built and running with an experiment active.

### Environment Variables Required

```
OPENAI_API_KEY=sk-proj-...
EXPERIMENTS_API_URL=http://localhost:1348
EXPERIMENT_ID=...
```

```bash

# Run with poetry (from root folder)
poetry run uvicorn deliverables.part1_api_and_containerization.app.main:app --reload

# Build with Docker (from root folder)
docker build -t ml-ops-api -f deliverables/part1_api_and_containerization/Dockerfile .

# Run with Docker (from root folder)
docker run -it -p 8000:8000 --env-file .env ml-ops-api:latest

docker-compose up --build

# Run tests (from root folder)
poetry run pytest

# Access the API
curl http://localhost:8000/health

curl -X POST http://localhost:8000/chat  \
     -H "Content-Type: application/json" \
    -d '{ "question": "hola", "user_id": "user_001", "conversation_id": "test-002"}'
```
