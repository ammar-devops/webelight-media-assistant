FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install only required OS packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        gcc \
        g++ \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first (best cache)
COPY requirements.prod.txt .

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.prod.txt

# Copy project
COPY . .

# Runtime folders
RUN mkdir -p uploads output database

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
CMD curl -fs http://localhost:8000/ || exit 1

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]