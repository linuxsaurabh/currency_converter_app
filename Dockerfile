FROM python:3.11-slim AS base

# Basic environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal build deps (remove cache after) - some packages may need a compiler
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY app .

# Create a non-root user and take ownership of the app directory
RUN groupadd --system app && useradd --system --gid app --create-home --home-dir /nonexistent app \
	&& chown -R app:app /app

USER app

EXPOSE 8080

# Use Gunicorn for production WSGI serving. The flask development server is not suitable for
# production and lacks robustness, performance and security features.
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "30"]
