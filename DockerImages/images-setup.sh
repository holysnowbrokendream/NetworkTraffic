#!/bin/bash

echo "========================================"
echo "Images Environment Configuration (Linux)"
echo "========================================"
echo

# Get host IP address
HOST_IP=$(hostname -I | awk '{print $1}')
echo "Detected host IP: $HOST_IP"
echo

# Create environment file
echo "Creating .env file for images deployment..."
cat > ../.env << EOF
# Images Environment Configuration
HOST_IP=$HOST_IP
ALLOWED_HOSTS=localhost,127.0.0.1,$HOST_IP,0.0.0.0,*
CSRF_TRUSTED_ORIGINS=http://localhost:23456,http://$HOST_IP:23456,http://127.0.0.1:23456,http://0.0.0.0:23456

# Database Configuration
DB_NAME=network_traffic
DB_USER=nwt_user
DB_PASSWORD=123456
DB_HOST=mysql
DB_PORT=3306
EOF

echo "Environment configuration created ✓"
echo
echo "Next steps:"
echo "1. Run ./start-services-images.sh to start services"
echo "2. Access application at: http://$HOST_IP:23456"
echo
