#!/bin/bash

echo "========================================"
echo "Docker Image Import Script (Linux)"
echo "========================================"
echo
echo "This script will import pre-built Docker images"
echo

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not running!"
    echo "Please install Docker and start the service, then try again."
    exit 1
fi
echo "Docker is running ✓"

# Import images
echo "Starting image import..."
echo

if [ -f "networktraffic-backend.tar" ]; then
    echo "Importing backend image..."
    if docker load -i "networktraffic-backend.tar"; then
        echo "Backend image imported successfully ✓"
    else
        echo "ERROR: Backend image import failed"
    fi
fi

if [ -f "networktraffic-frontend.tar" ]; then
    echo "Importing frontend image..."
    if docker load -i "networktraffic-frontend.tar"; then
        echo "Frontend image imported successfully ✓"
    else
        echo "ERROR: Frontend image import failed"
    fi
fi

if [ -f "mysql-8.0.tar" ]; then
    echo "Importing MySQL image..."
    if docker load -i "mysql-8.0.tar"; then
        echo "MySQL image imported successfully ✓"
    else
        echo "ERROR: MySQL image import failed"
    fi
fi

echo
echo "========================================"
echo "Step 2: Create Required Directories"
echo "========================================"
echo

echo "Creating necessary directories for the application..."
cd ..

# Create necessary directories
mkdir -p HTTP/media
mkdir -p HTTP/temp
mkdir -p HTTP/staticfiles
mkdir -p mysql/init
mkdir -p nginx/ssl
mkdir -p logs
echo "Directories created ✓"

echo
echo "========================================"
echo "Image Import Completed!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Ensure .env configuration file exists"
echo "2. Run ./start-services.sh to start services"
echo
