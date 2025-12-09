FROM python:3.12-slim

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libpangocairo-1.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir markdown2==2.5.4 weasyprint==66.0

# Copy the converter script
COPY convert.py /app/convert.py

# Create input and output directories
RUN mkdir -p /input /output

# Set the entrypoint
ENTRYPOINT ["python", "/app/convert.py"]
