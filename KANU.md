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

## Deploy (Terraform)
- Terraform files are in `infra/`
- Initialize: `cd infra && terraform init -backend-config=<your-backend-config>`
- Plan: `terraform plan -var="environment=beta" -var="db_name=..." -var="db_user=..." -var="db_host=..." -var="db_pass=..."`
- Apply: `terraform apply` (requires `lambda_package.zip` at repo root)
