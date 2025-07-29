# ---- Base Stage ----
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --default-timeout=100 --retries=5 -r requirements.txt

# ---- Final Stage ----
FROM python:3.10-slim AS final

WORKDIR /app

# Copy only installed packages from base
COPY --from=base /usr/local /usr/local

# Copy your source code
COPY . .

# Set environment variable (optional, can also use .env)
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "run.py"]
