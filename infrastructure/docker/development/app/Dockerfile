# Build stage
FROM python:3.12.1-slim-bookworm AS builder

# Install system dependencies
RUN apt-get update     && apt-get install -y --no-install-recommends     curl     gcc     python3-dev     && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/rembg_python

# Copy requirements
COPY requirements/base.txt requirements/dev.txt requirements/

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:/home/aguijarro/Software/visualaid/mlops_projects/rembg/venv/bin:/home/aguijarro/Software/flutter/development/flutter/bin:/home/aguijarro/.sdkman/candidates/springboot/current/bin:/home/aguijarro/.sdkman/candidates/java/current/bin:/home/aguijarro/.yarn/bin:/home/aguijarro/.config/yarn/global/node_modules/.bin:/home/aguijarro/.nvm/versions/node/v22.12.0/bin:/home/aguijarro/anaconda3/bin:/home/aguijarro/anaconda3/condabin:~/development/flutter/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin:/home/aguijarro/Android/Sdk/platform-tools"

RUN pip install --no-cache-dir --upgrade pip     && pip install --no-cache-dir -r requirements/base.txt     && pip install --no-cache-dir -r requirements/dev.txt

# Runtime stage
FROM python:3.12.1-slim-bookworm

LABEL maintainer="Andres Guijarro <ec.andres.guijarro@gmail.com>"
LABEL description="FastAPI development environment"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH="/opt/venv/bin:/home/aguijarro/Software/visualaid/mlops_projects/rembg/venv/bin:/home/aguijarro/Software/flutter/development/flutter/bin:/home/aguijarro/.sdkman/candidates/springboot/current/bin:/home/aguijarro/.sdkman/candidates/java/current/bin:/home/aguijarro/.yarn/bin:/home/aguijarro/.config/yarn/global/node_modules/.bin:/home/aguijarro/.nvm/versions/node/v22.12.0/bin:/home/aguijarro/anaconda3/bin:/home/aguijarro/anaconda3/condabin:~/development/flutter/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin:/home/aguijarro/Android/Sdk/platform-tools"     PYTHONPATH="/usr/rembg_python"

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set working directory
WORKDIR /usr/rembg_python

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Install curl for healthcheck
RUN apt-get update     && apt-get install -y --no-install-recommends curl     && rm -rf /var/lib/apt/lists/*

# Copy application code and test files
COPY --chown=appuser:appuser app app/
COPY --chown=appuser:appuser tests tests/
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser infrastructure/docker/development/.env.development app/.env

# Create pytest cache directory with correct permissions
RUN mkdir -p /tmp/.pytest_cache &&     chown -R appuser:appuser /tmp/.pytest_cache &&     chmod 777 /tmp/.pytest_cache

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3     CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

