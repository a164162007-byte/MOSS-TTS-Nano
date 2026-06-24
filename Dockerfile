FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git build-essential && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only with extra-index-url (primary PyPI + PyTorch CPU repo)
RUN pip install --no-cache-dir \
    torch==2.7.0 \
    torchaudio==2.7.0 \
    --extra-index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

RUN mkdir -p /app/models /app/generated_audio /app/.app_prompt_uploads
RUN chmod +x /app/entrypoint.sh

EXPOSE 18083

ENV HF_ENDPOINT=
ENV MODEL_DIR=/app/models
ENV OUTPUT_DIR=/app/generated_audio

ENTRYPOINT ["/app/entrypoint.sh"]
