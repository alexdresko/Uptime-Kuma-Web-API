#!/bin/bash
pip3 install --user -r requirements.txt

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