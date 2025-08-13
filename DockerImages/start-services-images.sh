#!/bin/bash

echo "========================================"
echo "Images Services Startup Script (Linux)"
echo "========================================"
echo

# Check if .env file exists
if [ ! -f ../.env ]; then
    echo "❌ .env file not found!"
    echo "Please run ./images-setup.sh first to configure the environment."
    exit 1
fi

# Check if Docker is running
echo "Checking Docker status..."
if ! docker --version > /dev/null 2>&1; then
    echo "❌ Docker is not running or not installed!"
    echo "Please start Docker service and try again."
    exit 1
fi
echo "Docker is running ✓"

# Check if Docker images exist
echo "Checking Docker images..."
if ! docker images | grep -q networktraffic; then
    echo "❌ NetworkTraffic Docker images not found!"
    echo "Please import Docker images first using ./import-images.sh"
    exit 1
fi
echo "Docker images found ✓"

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p ../config ../logs ../HTTP/media ../HTTP/staticfiles ../mysql/init ../nginx/ssl
echo "Directories created ✓"

# Start services
echo
echo "🚀 Starting NetworkTraffic services..."
if docker-compose -f ../docker-compose.client.yml up -d; then
    echo
    echo "✅ Services started successfully!"
    echo
    echo "📋 Service Status:"
    echo "  MySQL: localhost:3306"
    echo "  Backend: localhost:8000"
    echo "  Frontend: localhost:23456"
    echo "  Nginx: localhost:80"
    echo
    echo "🌐 Access URLs:"
    echo "  Frontend: http://localhost:23456"
    echo "  Backend API: http://localhost:8000"
    echo "  Admin: http://localhost:8000/admin/"
    echo
    echo "💡 To view logs: docker-compose -f ../docker-compose.client.yml logs -f"
    echo "💡 To stop services: docker-compose -f ../docker-compose.client.yml down"
    echo
else
    echo "❌ Failed to start services!"
    echo "Please check the error messages above."
    exit 1
fi
