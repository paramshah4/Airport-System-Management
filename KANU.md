# KANU.md

## Setup/Install
- Install Python dependencies: `pip install -r requirements.txt`
- Requires PostgreSQL database connection (psycopg2-binary==2.9.9)
- Package Lambda for deployment: `pip install -r requirements.txt -t ./package`

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
- Package Lambda: `cd package && zip -r ../lambda_package.zip . && cd .. && zip -g lambda_package.zip lambda_function.py`
- Initialize: `cd infra && terraform init -backend-config=<your-backend-config>`
- Plan: `terraform plan -var="environment=beta" -var="db_name=..." -var="db_user=..." -var="db_host=..." -var="db_pass=..." -var="db_port=..."`
- Apply: `terraform apply -auto-approve -var="environment=beta" -var="db_name=..." -var="db_user=..." -var="db_host=..." -var="db_pass=..." -var="db_port=..."`

## CI/CD (GitHub Actions)
- Beta deployment: `.github/workflows/beta.yml` triggers on PRs to `main`
- Prod deployment: `.github/workflows/prod.yml` triggers on push to `main` (i.e., merged PRs)
- Requires GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `TF_STATE_BUCKET`, `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PASS`, `DB_PORT`
