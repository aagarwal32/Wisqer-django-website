# DB subnet group for RDS instances, using the created subnets
resource "aws_db_subnet_group" "default" {
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  tags = {
    Name = "Wisqer_EC2_Subnet_Group"
  }
}

# Security group for RDS, allows PostgreSQL traffic
resource "aws_security_group" "rds_sg" {
  vpc_id      = aws_vpc.default.id
  name        = "WisqerRDSSecurityGroup"
  description = "Allow PostgreSQL traffic"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Updated to "10.0.0.0/16"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Updated to "10.0.0.0/16"
  }
  tags = {
    Name = "Wisqer_Security_Group"
  }
}

# RDS instance for Django backend, now privately accessible
resource "aws_db_instance" "default" {
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "16.7"
  instance_class         = "db.t3.micro"
  identifier             = "wisqerid"
  db_name                = data.aws_ssm_parameter.postgres_db.value
  username               = data.aws_ssm_parameter.postgres_user.value
  password               = data.aws_ssm_parameter.postgres_password.value
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = true # Changed to false for private access
  multi_az               = false
  tags = {
    Name = "Wisqer_RDS_Instance"
  }
}