#!/bin/bash
set -e

# If HF_ENDPOINT is set, configure huggingface_hub to use it
if [ -n "$HF_ENDPOINT" ]; then
    echo "Using HuggingFace mirror: $HF_ENDPOINT"
fi

# Start the ONNX web demo
exec python3 app_onnx.py \
    --host 0.0.0.0 \
    --port 18083 \
    --model-dir /app/models \
    --output-dir /app/generated_audio
