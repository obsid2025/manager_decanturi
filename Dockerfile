FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies + Chromium + ChromeDriver
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    chromium \
    chromium-driver \
    # Dependencies pentru Chromium headless
    libnss3 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    xvfb \
    # Additional dependencies pentru stabilitate
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Setează variabile de mediu pentru Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY automatizare_oblio_selenium.py .
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

# Run application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
