#!/bin/bash

# AWS ECR Deployment Script for CFDE IDG DRS API
# This script builds a Docker image and pushes it to AWS ECR

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration - UPDATE THESE VALUES
AWS_REGION="us-east-1"  # Change to your preferred region
AWS_ACCOUNT_ID=""  # Your AWS Account ID (will be auto-detected if empty)
ECR_REPOSITORY_NAME="cfde-idg-drs-api"
IMAGE_TAG="latest"

echo -e "${GREEN}=== CFDE IDG DRS API - ECR Deployment ===${NC}\n"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed.${NC}"
    echo "Please install it from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Please install it from: https://www.docker.com/"
    exit 1
fi

# Get AWS Account ID if not set
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo -e "${YELLOW}Getting AWS Account ID...${NC}"
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    if [ -z "$AWS_ACCOUNT_ID" ]; then
        echo -e "${RED}Error: Could not get AWS Account ID. Please configure AWS CLI.${NC}"
        exit 1
    fi
    echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}\n"
fi

# Set ECR repository URI
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  AWS Region: $AWS_REGION"
echo "  AWS Account: $AWS_ACCOUNT_ID"
echo "  ECR Repository: $ECR_REPOSITORY_NAME"
echo "  Image Tag: $IMAGE_TAG"
echo "  Full Image URI: ${ECR_URI}:${IMAGE_TAG}"
echo ""

# Check if ECR repository exists, if not create it
echo -e "${YELLOW}Checking if ECR repository exists...${NC}"
if ! aws ecr describe-repositories --repository-names "$ECR_REPOSITORY_NAME" --region "$AWS_REGION" &> /dev/null; then
    echo -e "${YELLOW}Repository doesn't exist. Creating ECR repository...${NC}"
    aws ecr create-repository \
        --repository-name "$ECR_REPOSITORY_NAME" \
        --region "$AWS_REGION" \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256
    echo -e "${GREEN}ECR repository created successfully!${NC}\n"
else
    echo -e "${GREEN}ECR repository already exists.${NC}\n"
fi

# Authenticate Docker to ECR
echo -e "${YELLOW}Authenticating Docker to ECR...${NC}"
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
echo -e "${GREEN}Docker authentication successful!${NC}\n"

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t "$ECR_REPOSITORY_NAME:$IMAGE_TAG" .
echo -e "${GREEN}Docker image built successfully!${NC}\n"

# Tag Docker image for ECR
echo -e "${YELLOW}Tagging Docker image for ECR...${NC}"
docker tag "$ECR_REPOSITORY_NAME:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
echo -e "${GREEN}Image tagged successfully!${NC}\n"

# Push Docker image to ECR
echo -e "${YELLOW}Pushing Docker image to ECR...${NC}"
docker push "$ECR_URI:$IMAGE_TAG"
echo -e "${GREEN}Image pushed successfully!${NC}\n"

echo -e "${GREEN}=== Deployment Complete! ===${NC}\n"
echo -e "Image URI: ${GREEN}${ECR_URI}:${IMAGE_TAG}${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Go to AWS App Runner console"
echo "2. Create a new service"
echo "3. Select 'Container registry' as source"
echo "4. Choose 'Amazon ECR' and select the repository: $ECR_REPOSITORY_NAME"
echo "5. Configure the service with:"
echo "   - Port: 8000"
echo "   - Environment variables (if needed for database connection)"
echo "6. Deploy the service"
echo ""
echo -e "${YELLOW}Important:${NC} Don't forget to set the DATABASE_URL environment variable in App Runner!"
