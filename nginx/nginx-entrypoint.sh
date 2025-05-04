#!/bin/sh
set -e

# Wait for certificates
while [ ! -f /etc/letsencrypt/live/zubies.com/fullchain.pem ]; do
  echo "Waiting for certificates..."
  sleep 5
done

# Start nginx
exec nginx -g "daemon off;"