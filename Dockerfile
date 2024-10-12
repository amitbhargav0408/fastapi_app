# Stage 1: Build the application
FROM python:3-alpine AS builder

WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3-alpine AS runner

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/venv venv

# Copy the application code
COPY app ./app
COPY api.yaml .
COPY README.md .

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose the application port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
