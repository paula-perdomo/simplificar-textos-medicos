#!/bin/bash
sudo pkill -f uvicorn

sudo docker stop biomedical-text-simplification
sudo docker rmi biomedical-text-simplification -f
