#!/bin/bash

# Ensure script stops on first error
set -e

echo "Starting deployment of P2P API Service..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Build and start the containers in detached mode
echo "Building and starting Docker containers..."
docker compose up -d --build

echo "Waiting for database to be ready..."
sleep 5

echo "Deployment successful!"
echo "API is running on http://localhost:8000"