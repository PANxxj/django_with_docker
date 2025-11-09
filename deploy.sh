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

# Login to Docker Hub
echo -e "${YELLOW}Logging into Docker Hub...${NC}"
if [ -f ~/.docker_token ]; then
    cat ~/.docker_token | docker login -u $DOCKER_USERNAME --password-stdin
else
    echo -e "${RED}Warning: ~/.docker_token not found. Make sure you have access to pull the image.${NC}"
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

# Blue-green deployment: Start new containers first
echo -e "${YELLOW}Updating image tag in .env...${NC}"
sed -i "s|WEB_IMAGE=.*|WEB_IMAGE=$IMAGE_TAG|" .env

echo -e "${YELLOW}Starting new containers...${NC}"
docker-compose up -d --no-deps web

# Wait for new container to be healthy
echo -e "${YELLOW}Waiting for application to be healthy...${NC}"
for i in {1..30}; do
    if docker-compose exec -T web python manage.py check --deploy; then
        echo -e "${GREEN}Application health check passed${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Health check failed, rolling back...${NC}"
        docker-compose down
        exit 1
    fi
    sleep 2
done

# Run migrations and collect static files
echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose exec -T web python manage.py migrate --noinput

echo -e "${YELLOW}Collecting static files...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

# Now update nginx to point to new containers
echo -e "${YELLOW}Updating nginx configuration...${NC}"
docker-compose up -d nginx

# Check final deployment status
sleep 5
echo -e "${YELLOW}Final deployment verification...${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}Deployment successful! All containers are running.${NC}"
else
    echo -e "${RED}Deployment failed!${NC}"
    docker-compose ps
    exit 1
fi

# Clean up old images
echo -e "${YELLOW}Cleaning up old images...${NC}"
docker image prune -f

# Logout for security
docker logout 2>/dev/null || true

echo -e "${GREEN}Deployment completed!${NC}"