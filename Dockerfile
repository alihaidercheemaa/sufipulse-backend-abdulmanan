# Multi-stage build to minimize container size
# Build stage
FROM python:3.11-slim as builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies in a separate virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install minimal system dependencies needed at runtime
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the working directory in the container
WORKDIR /app

# Copy the application code
COPY . .

# Make sure scripts in the virtual environment are usable
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port that the application runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]