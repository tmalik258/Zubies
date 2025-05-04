#!/bin/sh
set -e

# Wait for certificates with timeout
timeout=60
count=0
while [ ! -f /etc/letsencrypt/live/zubies.com/fullchain.pem ] && [ $count -lt $timeout ]; do
  echo "Waiting for certificates... ($count/$timeout)"
  sleep 5
  count=$((count + 5))
done

if [ ! -f /etc/letsencrypt/live/zubies.com/fullchain.pem ]; then
  echo "Certificate never appeared! Starting anyway..."
  exit 0
fi

exec nginx -g "daemon off;"