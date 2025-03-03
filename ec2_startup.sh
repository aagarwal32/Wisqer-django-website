#!/bin/bash
set -ex

# Update and install necessary packages
yum update -y
yum install -y yum-utils docker aws-cli

# Start and enable Docker
service docker start
systemctl enable docker

# Add ec2-user to Docker group (run Docker without sudo)
usermod -aG docker ec2-user

# Function to check if a new image is available
check_for_new_image() {
  LOCAL_DIGEST=$(docker images --digests --format "{{.Digest}}" 340752824077.dkr.ecr.us-east-1.amazonaws.com/wisqer-ecr:latest || true)
  REMOTE_DIGEST=$(aws ecr describe-images --repository-name wisqer-ecr --image-ids imageTag=latest --query 'imageDetails[0].imageDigest' --output text)

  if [[ "$LOCAL_DIGEST" != "$REMOTE_DIGEST" ]]; then
    echo "New image available. Pulling and restarting container..."
    return 0
  else
    echo "No new image available."
    return 1
  fi
}

# Authenticate to AWS ECR (initially)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 340752824077.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest Docker image from ECR and run the container (initially)
docker pull 340752824077.dkr.ecr.us-east-1.amazonaws.com/wisqer-ecr:latest
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

# Main loop to periodically check for new images
while true; do
  if check_for_new_image; then
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 340752824077.dkr.ecr.us-east-1.amazonaws.com
    docker pull 340752824077.dkr.ecr.us-east-1.amazonaws.com/wisqer-ecr:latest
    docker stop $(docker ps -q) || true
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
  fi
  sleep 300 # Wait for 5 minutes before checking for updates again
done