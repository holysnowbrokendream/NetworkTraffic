#!/bin/bash

# ========================================
# Docker镜像导出脚本 (Linux)
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
echo "Docker Image Export Script (Linux)"
echo "========================================"
echo
echo "This script will export successfully deployed Docker images to the specified directory"
echo

# Check if Docker is running
print_status "Checking Docker status..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not running!"
    echo "Please install Docker and start the service, then try again."
    exit 1
fi
print_success "Docker is running ✓"

# Create export directory
EXPORT_DIR="DockerImages"
mkdir -p "$EXPORT_DIR"
echo "Export directory: $EXPORT_DIR"

echo
echo "========================================"
echo "Step 1: Check Existing Images"
echo "========================================"
echo

# Check and list related images
print_status "Checking NetworkTraffic related images..."
if docker images | grep -q networktraffic; then
    docker images | grep networktraffic
else
    print_error "No NetworkTraffic images found, please run ./deploy-all.sh first to build images"
    exit 1
fi

echo
echo "========================================"
echo "Step 2: Export Images"
echo "========================================"
echo

# Export backend image
print_status "Exporting backend image..."
BACKEND_IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep networktraffic-backend | head -1)
if [ -n "$BACKEND_IMAGE" ]; then
    echo "Found backend image: $BACKEND_IMAGE"
    if docker save -o "$EXPORT_DIR/networktraffic-backend.tar" "$BACKEND_IMAGE"; then
        print_success "Backend image exported successfully: $EXPORT_DIR/networktraffic-backend.tar"
    else
        print_error "Backend image export failed"
    fi
else
    print_warning "Backend image not found, skipping export"
fi

# Export frontend image
echo
print_status "Exporting frontend image..."
FRONTEND_IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep networktraffic-frontend | head -1)
if [ -n "$FRONTEND_IMAGE" ]; then
    echo "Found frontend image: $FRONTEND_IMAGE"
    if docker save -o "$EXPORT_DIR/networktraffic-frontend.tar" "$FRONTEND_IMAGE"; then
        print_success "Frontend image exported successfully: $EXPORT_DIR/networktraffic-frontend.tar"
    else
        print_error "Frontend image export failed"
    fi
else
    print_warning "Frontend image not found, skipping export"
fi

# Export MySQL image (optional, as it uses official image)
echo
print_status "Exporting MySQL image (official image)..."
if docker save -o "$EXPORT_DIR/mysql-8.0.tar" mysql:8.0; then
    print_success "MySQL image exported successfully: $EXPORT_DIR/mysql-8.0.tar"
else
    print_error "MySQL image export failed"
fi

echo
echo "========================================"
echo "Export Completed!"
echo "========================================"
echo
echo "Exported files are located in: $EXPORT_DIR/"
echo
echo "Contains the following files:"
echo "✓ Backend image: networktraffic-backend.tar"
echo "✓ Frontend image: networktraffic-frontend.tar"  
echo "✓ MySQL image: mysql-8.0.tar"
echo "✓ Windows import script: import-images.bat"
echo "✓ Linux import script: import-images.sh"
echo "✓ Usage instructions: README.md"
echo
echo "Usage:"
echo "1. Copy the entire $EXPORT_DIR folder to others"
echo "2. Others can run the corresponding import script"
echo "3. No need to rebuild, start services directly"
echo
echo "Notes:"
echo "- Image files are large, please be patient during transfer"
echo "- Ensure target machine has sufficient disk space"
echo "- After import, you can use ./start-services.sh to start services"
echo
