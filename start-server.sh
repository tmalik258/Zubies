#!/bin/bash

# Script to update code and start the server

echo "Fetching latest changes from origin/main..."
git fetch origin main

echo "Rebasing current branch onto origin/main..."
git rebase origin/main

echo "Building and starting Docker containers..."
docker compose -f docker-compose.prod.yml up --build -d

echo "Server started successfully!"
