#!/bin/bash

# ========================================
# Complete Deployment Control Script (Linux)
# ========================================
# This script will:
# 1. Build the backend (Django + API)
# 2. Build the frontend (Vue.js)
# 3. Start all services (MySQL, Backend, Frontend)
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
echo "Complete Deployment Control Script (Linux)"
echo "========================================"
echo
echo "This script will:"
echo "1. Build the backend (Django + API)"
echo "2. Build the frontend (Vue.js)"
echo "3. Start all services (MySQL, Backend, Frontend)"
echo
echo "IMPORTANT NOTES:"
echo "- This process may take 10-20 minutes total"
echo "- Do not close this terminal during the build process"
echo "- Each step will pause for confirmation before proceeding"
echo
echo "Access URLs after deployment:"
echo "- Frontend: http://localhost:23456"
echo "- Backend: http://localhost:8000"
echo "- Database: localhost:3307"
echo
echo "Test accounts:"
echo "- Admin: admin/123456"
echo "- Test User: yang/123456"
echo

read -p "Press Enter to continue or Ctrl+C to abort..."

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

# Check if Docker Compose is available
if ! docker-compose --version > /dev/null 2>&1; then
    print_error "Docker Compose is not installed!"
    echo "Please install Docker Compose:"
    echo "sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "sudo chmod +x /usr/local/bin/docker-compose"
    exit 1
fi
print_success "Docker Compose is available ✓"

echo
echo "========================================"
echo "Step 1: Building Backend"
echo "========================================"
echo

print_status "Starting backend build..."
if ./build-backend.sh; then
    print_success "Backend build completed successfully ✓"
else
    print_error "Backend build failed!"
    echo "Please check the error messages above."
    exit 1
fi

echo
echo "========================================"
echo "Step 2: Building Frontend"
echo "========================================"
echo

print_status "Starting frontend build..."
if ./build-frontend.sh; then
    print_success "Frontend build completed successfully ✓"
else
    print_error "Frontend build failed!"
    echo "Please check the error messages above."
    exit 1
fi

echo
echo "========================================"
echo "Step 3: Starting Services"
echo "======================================="
echo

print_status "Starting all services..."
if ./start-services.sh; then
    print_success "Service startup completed successfully ✓"
else
    print_error "Service startup failed!"
    echo "Please check the error messages above."
    exit 1
fi

echo
echo "========================================"
echo "Deployment Completed Successfully!"
echo "========================================"
echo
echo "All components have been built and started:"
echo "✓ Backend (Django API)"
echo "✓ Frontend (Vue.js)"
echo "✓ Database (MySQL)"
echo
echo "Your application is now ready!"
echo
echo "Access URLs:"
echo "- Frontend Application: http://localhost:23456"
echo "- Backend API: http://localhost:8000"
echo "- Admin Interface: http://localhost:8000/admin/"
echo
echo "Test the application:"
echo "1. Open http://localhost:23456 in your browser"
echo "2. Login with admin/123456 or yang/123456"
echo "3. Try creating a new chat session"
echo "4. Test file upload and message sending"
echo
echo "Management commands:"
echo "- Stop all services: docker-compose -f docker-compose.production.yml down"
echo "- View logs: docker-compose -f docker-compose.production.yml logs -f"
echo "- Restart services: docker-compose -f docker-compose.production.yml restart"
echo
echo "========================================" 