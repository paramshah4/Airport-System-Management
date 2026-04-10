# KANU.md

## Setup

### Terraform Infrastructure
- Copy `infrastructure/terraform.tfvars.example` to `infrastructure/terraform.tfvars` and update values (especially `db_password`)
- Run `terraform init` in `infrastructure/` directory to initialize providers

## Run

## Deploy

### Terraform
- `cd infrastructure && terraform plan` - Preview infrastructure changes
- `cd infrastructure && terraform apply` - Deploy infrastructure to AWS
