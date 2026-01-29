FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install minimal runtime dependencies for the extras server
RUN pip install --no-cache-dir fastapi uvicorn jinja2 python-multipart

EXPOSE 8000

CMD ["uvicorn", "extras.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
