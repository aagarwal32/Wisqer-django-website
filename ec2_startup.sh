#!/bin/bash
set -ex
yum update -y
yum install -y yum-utils

# Install Docker
yum install -y docker
service docker start
systemctl enable docker

# Add ec2-user to Docker group (run Docker without sudo)
usermod -aG docker ec2-user

# Install AWS CLI
yum install -y aws-cli

# Authenticate to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 340752824077.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest Docker image from ECR
docker pull 340752824077.dkr.ecr.us-east-1.amazonaws.com/wisqer-ecr:latest

# Run the container with secrets injected
docker run -d -p 80:8080 \
  -e DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY}" \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
  -e POSTGRES_DB="${POSTGRES_DB}" \
  -e POSTGRES_USER="${POSTGRES_USER}" \
  -e POSTGRES_HOST="${POSTGRES_HOST}" \
  -e POSTGRES_PORT="${POSTGRES_PORT}" \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -e EMAIL_ID="${EMAIL_ID}" \
  -e EMAIL_PW="${EMAIL_PW}" \
  -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
  -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
  -e AWS_STORAGE_BUCKET_NAME="${AWS_STORAGE_BUCKET_NAME}" \
  340752824077.dkr.ecr.us-east-1.amazonaws.com/wisqer-ecr:latest