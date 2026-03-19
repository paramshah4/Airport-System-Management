terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "airport_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "airport-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.airport_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "airport-public-a"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.airport_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "airport-public-b"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "airport_igw" {
  vpc_id = aws_vpc.airport_vpc.id

  tags = {
    Name = "airport-igw"
  }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.airport_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.airport_igw.id
  }

  tags = {
    Name = "airport-public-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public_rt.id
}

# DB Subnet Group
resource "aws_db_subnet_group" "airport_db_subnet" {
  name       = "airport-db-subnet"
  subnet_ids = [aws_subnet.public_a.id, aws_subnet.public_b.id]

  tags = {
    Name = "airport-db-subnet"
  }
}

# Security Group
resource "aws_security_group" "airport_db_sg" {
  name        = "airport-db-sg"
  description = "Allow PostgreSQL inbound"
  vpc_id      = aws_vpc.airport_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "airport-db-sg"
  }
}

# Random Password
resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "airport_db" {
  identifier              = "airport-db"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  storage_type            = "gp2"
  db_name                 = "airport_db"
  username                = "airportadmin"
  password                = random_password.db_password.result
  publicly_accessible     = true
  skip_final_snapshot     = true
  db_subnet_group_name    = aws_db_subnet_group.airport_db_subnet.name
  vpc_security_group_ids  = [aws_security_group.airport_db_sg.id]

  tags = {
    Name = "airport-db"
  }
}

# Secrets Manager
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "airport-db-credentials"
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = aws_db_instance.airport_db.username
    password = random_password.db_password.result
    host     = aws_db_instance.airport_db.address
    port     = aws_db_instance.airport_db.port
    dbname   = aws_db_instance.airport_db.db_name
  })
}

# Database Initialization
resource "null_resource" "db_init" {
  triggers = {
    sql_hash = filemd5("${path.module}/init.sql")
  }

  provisioner "local-exec" {
    command = <<-EOT
      sudo apt-get update -qq && sudo apt-get install -y -qq postgresql-client > /dev/null 2>&1
      PGPASSWORD='${random_password.db_password.result}' psql -h ${aws_db_instance.airport_db.address} -p 5432 -U airportadmin -d airport_db -f ${path.module}/init.sql
    EOT
  }

  depends_on = [aws_db_instance.airport_db]
}
