FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Fix broken yarn repo (important)
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Install MediaPipe / OpenCV system libs
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
