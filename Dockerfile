FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (for psycopg2, Pillow, etc. if needed later)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files (important for production)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Production server
CMD ["gunicorn", "sunbeambackend.wsgi:application", "--bind", "0.0.0.0:8000"]
