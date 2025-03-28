#!/bin/bash

sudo apt update && apt-get install python3-venv -y

# Check if container already exists
if [ "$(docker ps -aq -f name=uptime-kuma)" ]; then
    echo "Container uptime-kuma already exists. Starting it if not running."
    if [ ! "$(docker ps -q -f name=uptime-kuma)" ]; then
        docker start uptime-kuma
    fi
else
    echo "Creating new uptime-kuma container"
    docker run -d --restart=always -p 3001:3001 -v ./data/uptime-kuma/data:/app/data --name uptime-kuma louislam/uptime-kuma:latest
fi

# Setup the application environment
echo "Setting up Uptime Kuma Web API..."

# Create and populate .env file with hardcoded values
touch /workspaces/Uptime-Kuma-Web-API/.env

ACCESS_TOKEN_EXPIRATION=5
SECRET_KEY=$(openssl rand -hex 32)

# Hardcoded values for development environment
KUMA_SERVER="http://localhost:3001"
KUMA_USERNAME="test"
KUMA_PASSWORD="Test&*()"
ADMIN_PASSWORD="Test&*()"

# Write to .env
echo "KUMA_SERVER=$KUMA_SERVER" > /workspaces/Uptime-Kuma-Web-API/.env
echo "KUMA_USERNAME=$KUMA_USERNAME" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "KUMA_PASSWORD=\"$KUMA_PASSWORD\"" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "ADMIN_PASSWORD=\"$ADMIN_PASSWORD\"" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "ACCESS_TOKEN_EXPIRATION=$ACCESS_TOKEN_EXPIRATION" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "SECRET_KEY=$SECRET_KEY" >> /workspaces/Uptime-Kuma-Web-API/.env

# Add run.sh environment variables
echo "NAME=uptime-kuma-web-api" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "WORKER_CLASS=uvicorn.workers.UvicornWorker" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "BIND=0.0.0.0:8000" >> /workspaces/Uptime-Kuma-Web-API/.env
echo "LOG_LEVEL=INFO" >> /workspaces/Uptime-Kuma-Web-API/.env

# Install dependencies
cd /workspaces/Uptime-Kuma-Web-API

# Make run.sh executable
chmod +x /workspaces/Uptime-Kuma-Web-API/run.sh

# Install requirements globally
pip install -r requirements.txt

# Run the application directly
export DIR=./app

# Check if .env exists and load it
if [ -f "./.env" ]; then
  export $(cat ./.env | xargs)
fi

if [ -z "$NAME" ]; then
  export NAME=uptime-kuma-web-api
fi

if [ -z "$WORKER_CLASS" ]; then
  export WORKER_CLASS=uvicorn.workers.UvicornWorker
fi

if [ -z "$BIND" ]; then
  export BIND=0.0.0.0:8000
fi

if [ -z "$LOG_LEVEL" ]; then
  export LOG_LEVEL=INFO
fi

cd $DIR

# Use the system gunicorn with reload for development
gunicorn main:app \
  --name $NAME \
  --workers 1 \
  --worker-class $WORKER_CLASS \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --reload