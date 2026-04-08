# KANU.md

## Setup/Install
- Install Python dependencies: `pip install -r requirements.txt`
- Requires PostgreSQL database connection (psycopg2-binary==2.9.9)

## Run
- Execute console application: `python console.py`

## Lambda Handler
- Entry point: `lambda_function.lambda_handler`
- Requires env vars: `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PASS`, `DB_PORT`
- Supports two actions via the event payload:
  - `"execute"`: runs custom SQL from `event["query"]`
  - `"query"`: runs a predefined query by `event["query_id"]` with `event["params"]`

## Deploy
- Package for AWS Lambda with psycopg2-binary dependency included
