#!/bin/bash

# ========================================
# Backend Build Script (Linux)
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
echo "Backend Build Script (Linux)"
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

# Create production environment file if not exists
if [ ! -f ".env" ]; then
    print_status "Creating production environment configuration..."
    cat > .env << 'EOF'
# ========================================
# Production Environment Configuration
# ========================================

# Database Configuration
DB_NAME=NetworkTraffic
DB_USER=nwt_user
DB_PASSWORD=123456
DB_HOST=mysql
DB_PORT=3307
MYSQL_ROOT_PASSWORD=123456

# Django Configuration
SECRET_KEY=network-traffic-production-secret-key-2024-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*,your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3001,http://localhost:23456,http://127.0.0.1:23456,http://0.0.0.0:23456,http://*:23456,https://your-domain.com,https://www.your-domain.com

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000

# Deployment Configuration
ENVIRONMENT=production

# Nginx Configuration
NGINX_SERVER_NAME=localhost
NGINX_SSL_CERT=/etc/nginx/ssl/cert.pem
NGINX_SSL_KEY=/etc/nginx/ssl/key.pem
EOF
    print_success "Production .env file created ✓"
fi

# Create necessary directories
print_status "Creating production directories..."
mkdir -p HTTP/media
mkdir -p HTTP/temp
mkdir -p HTTP/staticfiles
mkdir -p mysql/init
mkdir -p nginx/ssl
mkdir -p logs
print_success "Directories created ✓"

# Stop existing backend service
print_status "Stopping existing backend service..."
if docker-compose -f docker-compose.production.yml ps backend 2>/dev/null | grep -q "Up\|Exit"; then
    print_status "Backend container found, stopping it..."
    docker-compose -f docker-compose.production.yml stop backend 2>/dev/null || true
    docker-compose -f docker-compose.production.yml rm -f backend 2>/dev/null || true
    print_success "Backend service stopped ✓"
else
    print_status "No existing backend container found, skipping stop operation ✓"
fi

# Build backend image
print_status "Building backend Docker image..."
echo "This may take 5-10 minutes for the first build..."
echo "IMPORTANT: Do not close this terminal during the build process!"
echo

docker-compose -f docker-compose.production.yml build backend
if [ $? -ne 0 ]; then
    print_error "Backend Docker build failed!"
    echo "Please check the error messages above."
    exit 1
fi
print_success "Backend image built successfully ✓"

# Verify backend image was built
print_status "Verifying backend image..."
if docker images | grep -q "networktraffic-backend"; then
    print_success "Backend image verified ✓"
else
    print_error "Backend Docker image not found after build!"
    exit 1
fi

echo
echo "========================================"
echo "Backend Build Completed Successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Run build-frontend.sh to build the frontend"
echo "2. Run start-services.sh to start all services"
echo 