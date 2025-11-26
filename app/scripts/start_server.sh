#!/bin/bash
cd simplificar-textos-medicos/app
sudo docker build -t biomedical-text-simplification:latest .
sudo docker run --gpus all -p 8000:8000 biomedical-text-simplification:latest