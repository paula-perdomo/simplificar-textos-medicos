#!/bin/bash
pkill -f uvicorn

sudo docker stop biomedical-text-simplification
sudo docker rm biomedical-text-simplification
