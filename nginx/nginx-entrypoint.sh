#!/bin/sh
set -e

# Create certificate directory if missing
mkdir -p /etc/letsencrypt/live/zubies.com/

# Generate self-signed certificates if they don't exist
if [ ! -f /etc/letsencrypt/live/zubies.com/fullchain.pem ]; then
    echo "No SSL certificate found, creating self-signed certificate"
    
    # Generate private key and certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/zubies.com/privkey.pem \
        -out /etc/letsencrypt/live/zubies.com/cert.pem \
        -subj "/CN=zubies.com"
    
    # Create dummy chain files
    cat /etc/letsencrypt/live/zubies.com/cert.pem > /etc/letsencrypt/live/zubies.com/chain.pem
    cat /etc/letsencrypt/live/zubies.com/cert.pem > /etc/letsencrypt/live/zubies.com/fullchain.pem

    # Set permissions
    chmod -R 755 /etc/letsencrypt/live/
fi

# Start nginx
exec nginx -g "daemon off;"