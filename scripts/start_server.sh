#!/bin/bash

sudo docker run -d \
    --name biomedical-text-simplification \
    --restart unless-stopped \
    --gpus all \
    -p 8000:8000 \
    biomedical-text-simplification:latest