# 1. Base Image
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set S3 credentials
ENV S3_BUCKET_NAME="maia-grupo-9"
ENV S3_PREFIX="models/sft2-merged/"
ENV S3_REGION="us-east-2"
ENV MODEL_NAME="Llama-3.2-3B-Instruct"
ENV MODEL_PATH="./model/llm/"
ENV MODEL_SOURCE="s3"
ENV HF_TOKEN_SOURCE="aws"

ENV AWS_REGION="us-east-2"

# Ensure Rust is in the PATH for subsequent RUN instructions
ENV PATH="/root/.cargo/bin:${PATH}"

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies & Python 3.11
# We REMOVED 'cargo' from apt-get and added 'curl' to download rustup
RUN apt-get update && \
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
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Rust (Latest Stable) using rustup
# This fixes the "rustc too old" error
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# 6. Fix Python Alias
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# 7. Install Python Dependencies
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install packages
# Using --no-cache-dir to save space
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy Application Code
COPY . .

# 9. Expose Port
EXPOSE 8000

# 10. Run the Application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]