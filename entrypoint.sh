#!/bin/bash
set -e

if [ -n "$HF_ENDPOINT" ]; then
    echo "Using HuggingFace mirror: $HF_ENDPOINT"
fi

# Start via docker_entry.py (adds optional HTTP Basic Auth)
# Set WEB_USER and WEB_PASSWORD to enable authentication
exec python3 docker_entry.py \
    --host 0.0.0.0 \
    --port 18083 \
    --model-dir /app/models \
    --output-dir /app/generated_audio
