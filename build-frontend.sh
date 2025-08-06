#!/bin/bash

# ========================================
# Frontend Build Script (Linux)
# ========================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "========================================"
echo "Frontend Build Script (Linux)"
echo "========================================"

# Check if Docker is running
print_status "Checking Docker status..."
if ! docker --version > /dev/null 2>&1; then
    print_error "Docker is not running or not installed!"
    echo "Please install Docker and start the Docker service:"
    echo "sudo yum install -y docker"
    echo "sudo systemctl start docker"
    echo "sudo systemctl enable docker"
    exit 1
fi
print_success "Docker is running ✓"

# Check if Node.js is available
print_status "Checking Node.js..."
if ! node --version > /dev/null 2>&1; then
    print_error "Node.js is not installed or not in PATH!"
    echo "Please install Node.js:"
    echo "curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -"
    echo "sudo yum install -y nodejs"
    exit 1
fi
print_success "Node.js is available ✓"

# Check if npm is available
print_status "Checking npm..."
if ! npm --version > /dev/null 2>&1; then
    print_error "npm is not installed or not in PATH!"
    echo "Please install npm:"
    echo "sudo yum install -y npm"
    exit 1
fi
print_success "npm is available ✓"

# Stop existing frontend service
print_status "Stopping existing frontend service..."
if docker-compose -f docker-compose.production.yml ps frontend 2>/dev/null | grep -q "Up\|Exit"; then
    print_status "Frontend container found, stopping it..."
    docker-compose -f docker-compose.production.yml stop frontend 2>/dev/null || true
    docker-compose -f docker-compose.production.yml rm -f frontend 2>/dev/null || true
    print_success "Frontend service stopped ✓"
else
    print_status "No existing frontend container found, skipping stop operation ✓"
fi

# Build frontend application
print_status "Building frontend application..."
cd UI
if [ -d "dist" ]; then
    rm -rf dist
fi

print_status "Installing npm dependencies..."
echo "This may take several minutes..."
sleep 2
npm install --no-audit --no-fund
if [ $? -ne 0 ]; then
    print_error "npm install failed!"
    print_status "Trying alternative approach..."
    npm cache clean --force 2>/dev/null || true
    npm install --no-audit --no-fund
    if [ $? -ne 0 ]; then
        print_error "npm install still failed after cache clean!"
        cd ..
        exit 1
    fi
fi
print_success "npm dependencies installed ✓"

print_status "Building frontend with Vite..."
echo "This may take 1-3 minutes..."
sleep 2
npm run build
if [ $? -ne 0 ]; then
    print_error "Frontend build failed!"
    cd ..
    exit 1
fi
cd ..
print_success "Frontend built successfully ✓"

# Build frontend Docker image
print_status "Building frontend Docker image..."
echo "This may take 2-5 minutes for the first build..."
echo "IMPORTANT: Do not close this terminal during the build process!"
echo

docker-compose -f docker-compose.production.yml build frontend
if [ $? -ne 0 ]; then
    print_error "Frontend Docker build failed!"
    echo "Please check the error messages above."
    exit 1
fi
print_success "Frontend image built successfully ✓"

# Verify frontend image was built
print_status "Verifying frontend image..."
if docker images | grep -q "networktraffic-frontend"; then
    print_success "Frontend image verified ✓"
else
    print_error "Frontend Docker image not found after build!"
    exit 1
fi

echo
echo "========================================"
echo "Frontend Build Completed Successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Run build-backend.sh to build the backend (if not done)"
echo "2. Run start-services.sh to start all services"
echo 