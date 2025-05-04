#!/bin/sh
set -e

# Check if the certificate exists, if not, generate a self-signed one
if [ ! -f /etc/letsencrypt/live/zubies.com/fullchain.pem ]; then
    echo "No SSL certificate found, creating self-signed certificate"
    mkdir -p /etc/letsencrypt/live/zubies.com/
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/zubies.com/privkey.pem \
        -out /etc/letsencrypt/live/zubies.com/fullchain.pem \
        -subj "/CN=zubies.com"
    
    # Set permissions so nginx can read these files
    chmod -R 755 /etc/letsencrypt/live/
fi

# Start nginx
exec nginx -g "daemon off;"