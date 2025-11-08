#!/bin/bash

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting deployment...${NC}"

# Check if image tag is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Image tag not provided${NC}"
    echo "Usage: ./deploy.sh <image-tag>"
    exit 1
fi

IMAGE_TAG=$1
echo -e "${YELLOW}Deploying image: $IMAGE_TAG${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if docker and docker-compose are installed
if ! command_exists docker; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}Error: docker-compose is not installed${NC}"
    exit 1
fi

# Login to GitHub Container Registry
echo -e "${YELLOW}Logging into GitHub Container Registry...${NC}"
if [ -f ~/.github_token ]; then
    cat ~/.github_token | docker login ghcr.io -u $USER --password-stdin
else
    echo -e "${RED}Warning: ~/.github_token not found. Make sure you have access to pull the image.${NC}"
fi

# Pull the new image
echo -e "${YELLOW}Pulling image: $IMAGE_TAG${NC}"
if docker pull $IMAGE_TAG; then
    echo -e "${GREEN}Successfully pulled image${NC}"
else
    echo -e "${RED}Failed to pull image${NC}"
    exit 1
fi

# Stop current containers
echo -e "${YELLOW}Stopping current containers...${NC}"
docker-compose down

# Set the new image and start containers
echo -e "${YELLOW}Starting containers with new image...${NC}"
export WEB_IMAGE=$IMAGE_TAG
docker-compose up -d --force-recreate

# Check if containers are running
sleep 10
echo -e "${YELLOW}Checking container health...${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}Deployment successful! Containers are running.${NC}"
else
    echo -e "${RED}Warning: Some containers may not be running properly${NC}"
    docker-compose ps
fi

# Clean up old images
echo -e "${YELLOW}Cleaning up old images...${NC}"
docker image prune -f

# Logout for security
docker logout ghcr.io 2>/dev/null || true

echo -e "${GREEN}Deployment completed!${NC}"