#!/bin/bash
cd /home/ec2-user/simplificar-textos-medicos
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/uvicorn.log 2>&1 &
echo $! > /tmp/uvicorn.pid