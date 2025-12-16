#!/bin/sh
set -e

echo "🚀 Starting MinIO server..."

# Start MinIO server in background
minio server /data --console-address ":9001" &
MINIO_PID=$!

# Wait for MinIO to be ready
echo "⏳ Waiting for MinIO to start..."
sleep 8

# Configure MinIO client
echo "🔧 Configuring MinIO..."
mc alias set local http://127.0.0.1:9000 \
  "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}" || {
    echo "❌ Failed to configure MinIO client"
    exit 1
}

# Create buckets
echo "🪣 Creating buckets..."
mc mb -p local/static || echo "Bucket 'static' already exists"
mc mb -p local/media || echo "Bucket 'media' already exists"

# Set public access
echo "🔓 Setting bucket permissions..."
mc anonymous set public local/static || echo "Failed to set static bucket permissions"
mc anonymous set public local/media || echo "Failed to set media bucket permissions"

echo "✅ MinIO is ready!"
echo "   API: http://localhost:9000"
echo "   Console: http://localhost:9001"

# Keep MinIO running in foreground
wait $MINIO_PID
