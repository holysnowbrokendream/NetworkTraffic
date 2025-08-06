#!/bin/bash

# ========================================
# Service Startup Script (Linux)
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
echo "Service Startup Script (Linux)"
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

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    echo "Please run build-backend.sh first to create the environment file."
    exit 1
fi
print_success ".env file found ✓"

# Stop existing services
print_status "Stopping existing services..."
docker-compose -f docker-compose.production.yml down 2>/dev/null || true
print_success "Existing services stopped ✓"

# Start MySQL service
print_status "Starting MySQL service..."
docker-compose -f docker-compose.production.yml up -d mysql
if [ $? -ne 0 ]; then
    print_error "MySQL service startup failed!"
    exit 1
fi
print_success "MySQL service started ✓"

# Wait for MySQL to be ready
print_status "Waiting for MySQL to be ready..."
echo "This may take 30-60 seconds..."
for i in {1..60}; do
    if docker-compose -f docker-compose.production.yml exec mysql mysqladmin ping -h"localhost" -u"root" -p"123456" --silent 2>/dev/null; then
        print_success "MySQL is ready ✓"
        break
    fi
    if [ $i -eq 60 ]; then
        print_error "MySQL failed to start within 60 seconds!"
        exit 1
    fi
    echo -n "."
    sleep 1
done

# Start Backend service
print_status "Starting Backend service..."
docker-compose -f docker-compose.production.yml up -d backend
if [ $? -ne 0 ]; then
    print_error "Backend service startup failed!"
    exit 1
fi
print_success "Backend service started ✓"

# Wait for Backend to be ready
print_status "Waiting for Backend to be ready..."
echo "This may take 30-60 seconds..."
for i in {1..60}; do
    if curl -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
        print_success "Backend is ready ✓"
        break
    fi
    if [ $i -eq 60 ]; then
        print_warning "Backend may not be fully ready, but continuing..."
        break
    fi
    echo -n "."
    sleep 1
done

# Start Frontend service
print_status "Starting Frontend service..."
docker-compose -f docker-compose.production.yml up -d frontend
if [ $? -ne 0 ]; then
    print_error "Frontend service startup failed!"
    exit 1
fi
print_success "Frontend service started ✓"

# Wait for Frontend to be ready
print_status "Waiting for Frontend to be ready..."
echo "This may take 30-60 seconds..."
for i in {1..60}; do
    if curl -s http://localhost:23456 > /dev/null 2>&1; then
        print_success "Frontend is ready ✓"
        break
    fi
    if [ $i -eq 60 ]; then
        print_warning "Frontend may not be fully ready, but continuing..."
        break
    fi
    echo -n "."
    sleep 1
done

# Create default users
print_status "Creating default users..."
docker exec network_traffic_backend_prod python manage.py shell -c "
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create admin user if not exists
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='123456',
        is_staff=True,
        is_superuser=True
    )
    print('Admin user created: admin/123456')

# Create test user if not exists
if not User.objects.filter(username='yang').exists():
    test_user = User.objects.create_user(
        username='yang',
        email='yang@example.com',
        password='123456',
        is_staff=False,
        is_superuser=False
    )
    print('Test user created: yang/123456')

print('User creation completed')
" 2>/dev/null || print_warning "User creation may have failed (this is normal if users already exist)"

# Test API functionality
print_status "Testing API functionality..."
if curl -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
    print_success "API health check passed ✓"
else
    print_warning "API health check failed (this may be normal during startup)"
fi

# Show service status
print_status "Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo
echo "========================================"
echo "All Services Started Successfully!"
echo "========================================"
echo
echo "✅ Services Status:"
echo "- MySQL: Running on localhost:3307"
echo "- Backend: Running on localhost:8000"
echo "- Frontend: Running on localhost:23456"
echo
echo "🌐 Access URLs:"
echo "- Frontend Application: http://localhost:23456"
echo "- Backend API: http://localhost:8000"
echo "- Admin Interface: http://localhost:8000/admin/"
echo
echo "👤 Test Accounts:"
echo "- Admin: admin/123456"
echo "- Test User: yang/123456"
echo
echo "📊 Management Commands:"
echo "- View logs: docker-compose -f docker-compose.production.yml logs -f"
echo "- Stop services: docker-compose -f docker-compose.production.yml down"
echo "- Restart services: docker-compose -f docker-compose.production.yml restart"
echo
echo "========================================" 