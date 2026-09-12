# Multi-stage lightweight container for sovereign-avatar-agents
FROM python:3.11-slim as runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY n8n/ ./n8n/

RUN pip install --no-cache-dir -e .

EXPOSE 8785

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8785/healthz || exit 1

ENV PYTHONUNBUFFERED=1
ENV SBB_AVATAR_PORT=8785

ENTRYPOINT ["python3", "n8n/webhook_adapter.py"]
