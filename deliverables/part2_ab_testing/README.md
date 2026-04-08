# Part 2 — A/B Testing

Place your deliverables for Part 2 here.

## Expected Files

- Agent version files (Version A / Version B)
- Feature toggle / traffic split implementation
- `docs/measurement_plan.md` — Your experiment design document

## Files

For this part, a software component was created for managing the lifecycle of experiments through a REST API.

| File | Description |
|------|-------------|
| deliverables/part2_ab_testing/create_ab_test.sh | Script that makes a call to the experiments API to create a dummy experiment for the chatbot  |

Create experiment:
```bash
# change script to executable
chmod +x deliverables/part2_ab_testing/create_ab_test.sh

# execute
./deliverables/part2_ab_testing/create_ab_test.sh
```

*Important: Remember to update the .env file with the experiment id

## How to Run

```bash

# Run with poetry (from root folder)
poetry run uvicorn deliverables.part2_ab_testing.app.main:app --reload --port 1348

# Build with Docker (from root folder)
docker build -t ml-ops-experiments-api -f deliverables/part2_ab_testing/Dockerfile .

# Run with Docker (from root folder)
docker run -it -p 1348:1348 ml-ops-experiments-api:latest
```

## Technical Debt

TODO: implement unit tests