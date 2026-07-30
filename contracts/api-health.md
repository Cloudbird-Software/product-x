# API Contract: /health endpoint

## Endpoint

`GET /health`

## Request

No parameters, no body.

## Response

- Status: `200 OK`
- Content-Type: `application/json`
- Body:
  ```json
  {"status": "ok"}
  ```

## Assertions

1. Response status code is 200
2. Response body contains key `status` with value `ok`
