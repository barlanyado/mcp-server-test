# Install dependencies only when needed
FROM python:3.11 AS deps

RUN pip install --no-cache-dir mcp

WORKDIR /app

COPY . .

# Serve static files

CMD ["python", "app.py"]
