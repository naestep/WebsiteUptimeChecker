FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY uptime_checker.py .
COPY config.json .

# Create volume for logs
VOLUME ["/app/logs"]

# Run the uptime checker
CMD ["python", "uptime_checker.py"] 
