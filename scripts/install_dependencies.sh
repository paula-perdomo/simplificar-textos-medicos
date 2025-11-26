#!/bin/bash
cd /home/ubuntu/simplificar-textos-medicos/app

docker system prune -f
sudo docker build -t biomedical-text-simplification:latest .