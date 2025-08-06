#!/bin/bash

# ========================================
# Linux Firewall Configuration Script
# ========================================
# This script configures firewall rules for NetworkTraffic
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
echo "Linux Firewall Configuration Script"
echo "========================================"
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root (use sudo)"
    echo "Please run: sudo $0"
    exit 1
fi

print_success "Root privileges verified ✓"

# Detect Linux distribution
if command -v yum >/dev/null 2>&1; then
    # CentOS/RHEL
    FIREWALL_CMD="firewall-cmd"
    FIREWALL_SERVICE="firewalld"
elif command -v apt-get >/dev/null 2>&1; then
    # Ubuntu/Debian
    FIREWALL_CMD="ufw"
    FIREWALL_SERVICE="ufw"
else
    print_error "Unsupported Linux distribution"
    exit 1
fi

print_status "Detected firewall system: $FIREWALL_CMD"

# Function to configure firewalld (CentOS/RHEL)
configure_firewalld() {
    print_status "Configuring firewalld..."
    
    # Start and enable firewalld
    systemctl start firewalld
    systemctl enable firewalld
    
    # Add ports to firewall
    firewall-cmd --permanent --add-port=8000/tcp
    firewall-cmd --permanent --add-port=23456/tcp
    firewall-cmd --permanent --add-port=3307/tcp
    
    # Reload firewall
    firewall-cmd --reload
    
    print_success "Firewalld configured successfully ✓"
}

# Function to configure ufw (Ubuntu/Debian)
configure_ufw() {
    print_status "Configuring ufw..."
    
    # Enable ufw
    ufw --force enable
    
    # Add ports to firewall
    ufw allow 8000/tcp
    ufw allow 23456/tcp
    ufw allow 3307/tcp
    
    print_success "UFW configured successfully ✓"
}

# Configure firewall based on detected system
if [[ "$FIREWALL_CMD" == "firewall-cmd" ]]; then
    configure_firewalld
elif [[ "$FIREWALL_CMD" == "ufw" ]]; then
    configure_ufw
fi

# Configure iptables as backup (for older systems)
print_status "Configuring iptables rules..."
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
iptables -A INPUT -p tcp --dport 23456 -j ACCEPT
iptables -A INPUT -p tcp --dport 3307 -j ACCEPT

# Save iptables rules
if command -v iptables-save >/dev/null 2>&1; then
    iptables-save > /etc/iptables/rules.v4 2>/dev/null || \
    iptables-save > /etc/sysconfig/iptables 2>/dev/null || \
    print_warning "Could not save iptables rules (this is normal)"
fi

print_success "Iptables rules configured ✓"

echo
echo "========================================"
echo "Firewall Configuration Complete!"
echo "========================================"
echo
echo "✅ Configured ports:"
echo "- 8000: Backend API Service"
echo "- 23456: Frontend Web Service"
echo "- 3307: Database Service (optional)"
echo
echo "💡 Now devices on the same network can access your services"
echo
echo "To verify firewall status:"
if [[ "$FIREWALL_CMD" == "firewall-cmd" ]]; then
    echo "- Check firewalld: firewall-cmd --list-ports"
elif [[ "$FIREWALL_CMD" == "ufw" ]]; then
    echo "- Check ufw: ufw status"
fi
echo "- Check iptables: iptables -L"
echo
echo "========================================" 