resource "aws_iam_role" "lambda_role" {
  name = "airport-management-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "airport_management" {
  function_name    = "airport_management_${var.environment}"
  filename         = "${path.module}/../lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda_package.zip")
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  role             = aws_iam_role.lambda_role.arn

  environment {
    variables = {
      DB_NAME = var.db_name
      DB_USER = var.db_user
      DB_HOST = var.db_host
      DB_PASS = var.db_pass
      DB_PORT = var.db_port
    }
  }
}
