#!/bin/bash

# ========================================
# Network Access Configuration Script (Linux)
# ========================================
# This script configures Django application for network access
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
echo "Network Access Configuration Script (Linux)"
echo "========================================"
echo

# Check if Python is available
print_status "Checking Python environment..."
if ! python3 --version > /dev/null 2>&1; then
    print_error "Python3 is not installed or not in PATH"
    echo "Please install Python3:"
    echo "sudo yum install -y python3"
    exit 1
fi
print_success "Python3 environment check passed ✓"

# Run network configuration script
echo
print_status "Starting network access configuration..."
python3 network_access_config.py

if [ $? -ne 0 ]; then
    print_error "Network configuration script execution failed"
    exit 1
fi

echo
echo "========================================"
echo "Network Access Configuration Complete!"
echo "========================================"
echo
echo "💡 Next steps:"
echo "1. Rebuild backend: ./build-backend.sh"
echo "2. Restart services: ./start-services.sh"
echo "3. Test network access"
echo
echo "⚠️  Important notes:"
echo "- Ensure firewall allows ports 8000 and 23456"
echo "- Devices on the same network can access via server IP"
echo "- If access fails, check firewall settings"
echo
echo "========================================" 