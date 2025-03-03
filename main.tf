# Defines AWS provider and sets the region for resource provisioning
provider "aws" {
  region = "us-east-1"
  profile = "default"
}


# Creates a Virtual Private Cloud to isolate the infrastructure
resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "Wisqer_VPC"
  }
}


# Internet Gateway to allow internet access to the VPC
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = {
    Name = "Wisqer_Internet_Gateway"
  }
}


# Route table for controlling traffic leaving the VPC
resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
  tags = {
    Name = "Wisqer_Route_Table"
  }
}


# Subnet within VPC for resource allocation, in availability zone us-east-1a
resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "us-east-1a"
  tags = {
    Name = "Wisqer_Subnet_1"
  }
}


# Subnet 2 for redundancy, in availability zone us-east-1b
resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "us-east-1b"
  tags = {
    Name = "Wisqer_Subnet_2"
  }
}


# Associate subnets with route table for internet access
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.default.id
}
resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.default.id
}


# Security group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  vpc_id = aws_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
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
    Name = "Wisqer_Security_Group"
  }
}


# EC2 instance for the local web app
resource "aws_instance" "web" {
  ami                    = "ami-0c101f26f147fa7fd" # Amazon Linux
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.subnet1.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  associate_public_ip_address = true
  user_data_replace_on_change = true

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  # Inject secrets from AWS SSM into startup script
  user_data = templatefile("${path.module}/ec2_startup.sh", {
    DJANGO_SECRET_KEY = data.aws_ssm_parameter.django_secret_key.value,
    POSTGRES_PASSWORD = data.aws_ssm_parameter.postgres_password.value,
    POSTGRES_DB = data.aws_ssm_parameter.postgres_db.value,
    POSTGRES_USER = data.aws_ssm_parameter.postgres_user.value,
    POSTGRES_HOST = data.aws_ssm_parameter.postgres_host.value,
    POSTGRES_PORT = data.aws_ssm_parameter.postgres_port.value,
    OPENAI_API_KEY = data.aws_ssm_parameter.openai_api_key.value,
    EMAIL_ID = data.aws_ssm_parameter.email_id.value,
    EMAIL_PW = data.aws_ssm_parameter.email_pw.value,
    AWS_ACCESS_KEY_ID = data.aws_ssm_parameter.aws_access_key_id.value,
    AWS_SECRET_ACCESS_KEY = data.aws_ssm_parameter.aws_secret_access_key.value,
    AWS_STORAGE_BUCKET_NAME = data.aws_ssm_parameter.aws_storage_bucket_name.value,
  })

  tags = {
    Name = "Wisqer_Complete_Server"
  }
}


# IAM role for EC2 instance to access ECR
resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "ec2.amazonaws.com",
      },
      Effect = "Allow",
    }],
  })
}


# Attach the AmazonEC2ContainerRegistryReadOnly policy to the role
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}


# IAM instance profile for EC2 instance
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "django_ec2_complete_profile"
  role = aws_iam_role.ec2_role.name
}


# SECRETS -- AWS SSM PARAMETER STORE
data "aws_ssm_parameter" "django_secret_key" {
  name = "/wisqer/django_secret_key"
}

data "aws_ssm_parameter" "postgres_password" {
  name = "/wisqer/postgres_password"
}

data "aws_ssm_parameter" "postgres_db" {
  name = "/wisqer/postgres_db"
}

data "aws_ssm_parameter" "postgres_user" {
  name = "/wisqer/postgres_user"
}

data "aws_ssm_parameter" "postgres_host" {
  name = "/wisqer/postgres_host"
}

data "aws_ssm_parameter" "postgres_port" {
  name = "/wisqer/postgres_port"
}

data "aws_ssm_parameter" "openai_api_key" {
  name = "/wisqer/openai_api_key"
}

data "aws_ssm_parameter" "email_id" {
  name = "/wisqer/email_id"
}

data "aws_ssm_parameter" "email_pw" {
  name = "/wisqer/email_pw"
}

data "aws_ssm_parameter" "aws_access_key_id" {
  name = "/wisqer/aws_access_key_id"
}

data "aws_ssm_parameter" "aws_secret_access_key" {
  name = "/wisqer/aws_secret_access_key"
}

data "aws_ssm_parameter" "aws_storage_bucket_name" {
  name = "/wisqer/aws_storage_bucket_name"
}
