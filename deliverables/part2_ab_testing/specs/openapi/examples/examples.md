# Examples using CURL

## Create a New Experiment

Endpoint: POST /experiment
Description: Initializes an experiment. Validates that the sum of traffic equals 1.0.

Request:
```bash
curl -X POST http://api.ml-experiments.io/experiment \
-H "Content-Type: application/json" \
-d '{
  "model_id": "550e8400-e29b-41d4-a716-446655440000",
  "variants": [
    { "name": "control", "traffic": 0.8 },
    { "name": "treatment_a", "traffic": 0.2 }
  ],
  "tags": ["vision", "beta-test"]
}'
```

Success Response (201 Created):
```json
{
  "id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "model_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PENDING",
  "metrics": {},
  "created_at": "2026-04-06T22:30:00Z"
}
```

## Update Experiment Status

Endpoint: PUT /experiment/{id}
Description: Moves the experiment through the state machine (e.g., from PENDING to RUNNING).

Request:
```bash
curl -X PUT http://api.ml-experiments.io/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6 \
-H "Content-Type: application/json" \
-d '{
  "status": "RUNNING",
  "tags": ["vision", "beta-test", "active"]
}'
```

Success Response (200 OK):
```json
{
  "message": "Experiment updated"
}
```

## Archive an Experiment (Soft Delete)

Endpoint: DELETE /experiment/{id}
Description: Logical deletion. The experiment status changes to ARCHIVED.

Request:
```bash
curl -X DELETE http://api.ml-experiments.io/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6
```

Success Response (204 No Content)


## Get Experiment Details

Endpoint: GET /experiment/{id}
Description: Retrieves metadata. Includes include-archive query parameter to find logically deleted items.

Request:
```bash
curl -X GET "http://api.ml-experiments.io/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6?include-archive=true" \
-H "Accept: application/json"
```

Success Response (200 OK):
```json
{
  "id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "model_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "ARCHIVED",
  "metrics": {
    "accuracy": 0.94
  },
  "created_at": "2026-04-06T22:30:00Z"
}
```

## Get Experiment Data

Endpoint: GET /experiment/{id}/data
Description: Accesses raw results or artifact references.

Request:
```bash
curl -X GET http://api.ml-experiments.io/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6/data
```

Success Response (200 OK):
```json
{
  "raw_logs_uri": "s3://ml-experiments/logs/a1b2c3d4.parquet",
  "feature_importance": {
    "feature_1": 0.45,
    "feature_2": 0.55
  }
}
```