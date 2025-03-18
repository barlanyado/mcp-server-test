# Install dependencies only when needed
FROM python:3.11 AS deps



WORKDIR /app


COPY . .

RUN pip install --no-cache-dir mcp
# Serve static files

CMD ["python", "app.py"]
