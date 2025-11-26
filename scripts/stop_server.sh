#!/bin/bash
sudo pkill -f uvicorn

# Stop the container if it exists
sudo docker stop biomedical-text-simplification || true

# Remove the container so we can reuse the name
sudo docker rm biomedical-text-simplification || true
