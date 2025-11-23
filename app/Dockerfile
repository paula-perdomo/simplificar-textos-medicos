# 1. Base Image
# We MUST use an NVIDIA CUDA image to access the GPU on the g4dn instance.
# "runtime" includes the CUDA libraries needed to run PyTorch.
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 2. Set Environment Variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures logs and output are sent straight to the console
ENV PYTHONUNBUFFERED 1

# Set S3 credentials
ENV S3_BUCKET_NAME="maia-grupo-9"
ENV S3_PREFIX="/models/sft2-merged/"
ENV S3_REGION="us-east-2"
ENV MODEL_NAME="Llama-3.2-3B-Instruct"
ENV MODEL_PATH="./model/llm/"
ENV MODEL_SOURCE="s3"
ENV HF_TOKEN_SOURCE="aws"

ENV AWS_REGION="us-east-2"

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies & Python 3.11
# The base Ubuntu 22.04 image comes with Python 3.10.
# We add the deadsnakes PPA to get Python 3.11 explicitly.

# Install tzdata
RUN apt-get update &&\
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
    
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Fix Python Alias
# Ensure 'python' and 'python3' point to python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# 6. Install Python Dependencies
COPY requirements.txt .

# Upgrade pip to ensure compatibility
RUN python -m pip install --upgrade pip

# Install packages. 
# Note: Ensure your requirements.txt includes a version of torch compatible with CUDA 12.1
# e.g., --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy Application Code
COPY . .

# 8. Expose Port
EXPOSE 8000

# 9. Run the Application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]