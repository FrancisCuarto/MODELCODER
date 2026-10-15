# Multi-stage lightweight Dockerfile for ModelCoder On-Demand Generation Worker
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    BLENDER_VERSION=4.2.0 \
    BLENDER_URL=https://download.blender.org/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz

# Install system dependencies required for headless Blender rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    xz-utils \
    libx11-6 \
    libxxf86vm1 \
    libxcursor1 \
    libxi6 \
    libxrandr2 \
    libxinerama1 \
    libegl1 \
    libopengl0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Download and extract Blender Linux binary
WORKDIR /opt
RUN wget -q $BLENDER_URL && \
    tar -xf blender-4.2.0-linux-x64.tar.xz && \
    rm blender-4.2.0-linux-x64.tar.xz && \
    ln -s /opt/blender-4.2.0-linux-x64/blender /usr/local/bin/blender

WORKDIR /app

# Copy application files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
