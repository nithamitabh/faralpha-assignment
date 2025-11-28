FROM python:3.9-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port (not required but good practice)
EXPOSE 5000

ENV PORT=5000

CMD ["python", "app.py"]
