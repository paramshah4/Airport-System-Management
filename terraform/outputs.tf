output "rds_endpoint" {
  description = "RDS instance endpoint hostname"
  value       = aws_db_instance.airport_db.address
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.airport_db.port
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.airport_db.db_name
}

output "db_username" {
  description = "Database master username"
  value       = aws_db_instance.airport_db.username
}

output "db_password" {
  description = "Database master password"
  value       = random_password.db_password.result
  sensitive   = true
}

output "secrets_manager_secret_arn" {
  description = "ARN of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}
