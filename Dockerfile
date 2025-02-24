FROM python:3.11-slim

RUN apt-get update && apt-get install -y redis-server \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy dependency lists and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Expose the port your app will run on
EXPOSE 80

# Start redis-server, celery worker, and uvicorn.
CMD redis-server --daemonize yes && \
    celery -A main worker & \
    uvicorn main:api --host 0.0.0.0 --port 80
