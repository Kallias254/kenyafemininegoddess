# KFGAPP/Dockerfile

# 1. Base Image:
    FROM python:3.12-slim-bookworm

    # 2. Environment Variables:
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # 3. Set Work Directory:
    WORKDIR /app
    
    # 4. Install System Dependencies:
    RUN apt-get update && apt-get install -y --no-install-recommends \
        # For psycopg2-binary (already had these, good)
        libpq-dev \
        gcc \
        # For Pillow (common dependencies)
        libjpeg62-turbo-dev \
        zlib1g-dev \
        # Optional, but good for broader Pillow support:
        # libwebp-dev \
        # libtiff-dev \
        # libopenjp2-7-dev \
        # build-essential \ # Sometimes a more general package for build tools
        && rm -rf /var/lib/apt/lists/*
    
    # 5. Copy and Install Python Dependencies:
    COPY requirements.txt /app/
    RUN pip install --no-cache-dir -r requirements.txt
    
    # 6. Copy Project Code:
    COPY . /app/
    
    # 7. Run collectstatic:
    RUN python manage.py collectstatic --noinput --clear
    
    # 8. Expose Port:
    EXPOSE 8000
    
    # 9. Run Gunicorn:
    CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]