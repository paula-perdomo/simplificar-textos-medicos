#!/bin/bash
cd /home/ec2-user/simplificar-textos-medicos/app
sudo docker run --gpus all -p 8000:8000 biomedical-text-simplification:latest