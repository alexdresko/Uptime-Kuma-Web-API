#!/bin/bash
pip3 install --user -r requirements.txt

docker run -d --restart=always -p 3001:3001 -v ./data/uptime-kuma/data:/app/data --name uptime-kuma louislam/uptime-kuma:latest