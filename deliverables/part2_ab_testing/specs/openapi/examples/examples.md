# Examples using CURL

## Create a New Experiment

Endpoint: POST /experiment
Description: Initializes an experiment. Validates that the sum of traffic equals 1.0.

Request:
```bash
curl -X POST http://localhost:1348/experiment \
-H "Content-Type: application/json" \
-d '{
  "name": "Recommender Algorithm V2",
  "hypothesis": "Switching to Transformer-based embeddings will increase CTR by 5%.",
  "description": "Testing new embedding logic vs the baseline matrix factorization.",
  "variants": [
    { 
      "name": "control", 
      "control": true, 
      "traffic": 0.8,
      "config": { "model_version": "v1.2.0" }
    },
    { 
      "name": "treatment_a", 
      "control": false, 
      "traffic": 0.2,
      "config": { "model_version": "v2.0.0-beta" }
    }
  ]
}'
```

Success Response (201 Created):
```json
{
  "id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "name": "Recommender Algorithm V2",
  "hypothesis": "Switching to Transformer-based embeddings will increase CTR by 5%.",
  "description": "Testing new embedding logic vs the baseline matrix factorization.",
  "status": "PENDING",
  "created_at": "2026-04-07T16:00:00Z",
  "variants": [
    { "name": "control", "control": true, "traffic": 0.8, "config": { "model_version": "v1.2.0" } },
    { "name": "treatment_a", "control": false, "traffic": 0.2, "config": { "model_version": "v2.0.0-beta" } }
  ]
}
```

## Update Experiment Status

Endpoint: PUT /experiment/{id}
Description: Moves the experiment through the state machine (e.g., from PENDING to RUNNING).

Request:
```bash
curl -X PUT http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6 \
-H "Content-Type: application/json" \
-d '{
  "status": "RUNNING",
  "tags": ["vision", "production", "sprint-42"]
}'
```

Success Response (200 OK No Content) 

## Archive an Experiment (Soft Delete)

Endpoint: DELETE /experiment/{id}
Description: Logical deletion. The experiment status changes to ARCHIVED.

Request:
```bash
curl -X DELETE http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6
```

Success Response (204 No Content)

## Get User Variant Assignment

Endpoint: GET /experiment/{id}/user/{user_id}/variant
Description: High-latency optimized endpoint to retrieve the specific variant assigned to a user.

Request:
```bash
curl -X GET http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6/user/1096035447/variant
```

Success Response (200 OK):
```bash
{
  "name": "treatment_a",
  "control": false,
  "traffic": 0.2,
  "config": {
    "model_version": "v2.0.0-beta"
  }
}
```

## Post Experiment Metric

Endpoint: POST /experiment/{id}/user/{user_id}/metric
Description: Records a metric event for a user. Designed for low-latency ingestion.
Request:
```bash
curl -X POST http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6/user/f47ac10b-58cc-4372-a567-0e02b2c3d479/metric \
-H "Content-Type: application/json" \
-d '{
  "metric_key": "click_rate",
  "value": 1.0,
  "timestamp": "2026-04-07T16:10:00Z"
}'
```

Success Response (204 No Content)

## Get Experiment Data

Endpoint: GET /experiment/{id}/data

Description: Retrieves aggregated results or raw data references for the experiment.

Request:
```bash
curl -X GET http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6/data
```

Success Response (200 OK):
```json
{
  "columns": ["user_id", "variant_name", "timestamp", "metric_key", "value"],
  "data": [
    ["1096035447", "variant_a", "2026-04-07T16:10:00Z", "click_rate", 1.0],
    ["7505211", "control", "2026-04-07T11:10:00Z", "click_rate", 0.0],
    ["1096034447", "control", "2026-03-07T16:10:00Z", "click_rate", 1.0],
  ]
}
```



## Get Experiment Details

Endpoint: GET /experiment/{id}
Description: Retrieves metadata. Includes include-archive query parameter to find logically deleted items.

Request:
```bash
curl -X GET "http://localhost:1348/experiment/a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6?include-archive=true" \
-H "Accept: application/json"
```

Success Response (200 OK):
```json
{
  "id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "name": "Recommender Algorithm V2",
  "hypothesis": "Switching to Transformer-based embeddings will increase CTR by 5%.",
  "description": "Testing new embedding logic vs the baseline matrix factorization.",
  "status": "PENDING",
  "created_at": "2026-04-07T16:00:00Z",
  "variants": [
    { "name": "control", "control": true, "traffic": 0.8, "config": { "model_version": "v1.2.0" } },
    { "name": "treatment_a", "control": false, "traffic": 0.2, "config": { "model_version": "v2.0.0-beta" } }
  ]
}
```
