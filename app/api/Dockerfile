# 1. Base Image
# Use an official Python slim-buster image for a good balance of size and compatibility.
FROM python:3.10-slim

# 2. Set Environment Variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures logs and output are sent straight to the console
ENV PYTHONUNBUFFERED 1
# Set model name and path
ENV MODEL_NAME="Llama-3.2-3B-Instruct"
ENV MODEL_PATH="meta-llama/Llama-3.2-3B-Instruct"

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies
# 'git' is required to install the AlignScore package from its GitHub URL.
# We clean up apt caches to keep the final image slim.
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
# Copy requirements.txt first to leverage Docker's layer caching.
# This layer only rebuilds if requirements.txt changes.
COPY requirements.txt .

# Install packages, using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# 6. Add Hugging Face Login (Secure Method)
# This command tells Docker to securely mount the secret file we will provide.
# The token is used for the login and then discarded.
# It is NEVER saved in the image layers.
RUN --mount=type=secret,id=hf_token \
    huggingface-cli login --token $(cat /run/secrets/hf_token)

# 7. Copy Application Code
# Copy the rest of the app's source code (main.py, models, etc.)
# into the container.
COPY . .

# 8. Expose Port
# Tell Docker the container listens on port 8000.
EXPOSE 8000

# 9. Run the Application
# The command to start the uvicorn server.
# We use 0.0.0.0 to make it accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]