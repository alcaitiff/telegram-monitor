#!/bin/bash

# === CONFIG ===
IMAGE_NAME="telegram-monitor"
CONTAINER_NAME="telegram-monitor"
ENV_FILE=".env"

# === CHECK ARGUMENT ===
if [ -z "$1" ]; then
    echo "Usage: $0 /full/path/to/watched/folder"
    exit 1
fi

WATCHED_HOST_DIR="$1"

# === CHECK IF FOLDER EXISTS ===
if [ ! -d "$WATCHED_HOST_DIR" ]; then
    echo "❌ Error: Folder '$WATCHED_HOST_DIR' does not exist."
    exit 1
fi

# === CHECK IF .env EXISTS ===
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: '$ENV_FILE' file not found. Please create one with TELEGRAM_TOKEN, TELEGRAM_USER_ID, and WATCHED_FOLDER."
    exit 1
fi

if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "🔨 Image not found. Building Docker image '$IMAGE_NAME'..."
    docker build -t "$IMAGE_NAME" .
else
    echo "✅ Docker image '$IMAGE_NAME' already exists. Skipping build."
fi

# === STOP AND REMOVE EXISTING CONTAINER ===
if docker ps -aq -f name="$CONTAINER_NAME" > /dev/null; then
    echo "🧹 Removing existing container..."
    docker rm -f "$CONTAINER_NAME"
fi

# === RUN CONTAINER ===
echo "🚀 Running container..."
docker run -d \
    --env-file "$ENV_FILE" \
    -v "$WATCHED_HOST_DIR":/watched \
    --name "$CONTAINER_NAME" \
    "$IMAGE_NAME"

echo "✅ Bot is now monitoring: $WATCHED_HOST_DIR"
