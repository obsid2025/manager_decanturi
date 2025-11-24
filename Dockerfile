FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies + Chromium + ChromeDriver
# Instalăm DOAR esențialele - Debian instalează automat dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    chromium \
    chromium-driver \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to Bucharest
ENV TZ=Europe/Bucharest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Setează variabile de mediu pentru Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY automatizare_oblio_selenium.py .
COPY database.py .
COPY templates ./templates/
COPY static ./static/

# Create directories for uploads and exports
RUN mkdir -p uploads exports

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application with eventlet (pentru WebSocket support)
# IMPORTANT: Gunicorn standard NU suportă WebSocket!
# Folosim direct Python cu socketio.run() care folosește eventlet
CMD ["python", "app.py"]
