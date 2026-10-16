FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install Node.js 20 LTS & dependencies for headless Blender 3D rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
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
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install official Blender 4.2 Linux x64
WORKDIR /opt
RUN wget -q https://download.blender.org/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz && \
    tar -xf blender-4.2.0-linux-x64.tar.xz && \
    rm blender-4.2.0-linux-x64.tar.xz && \
    ln -s /opt/blender-4.2.0-linux-x64/blender /usr/local/bin/blender

WORKDIR /workspace
