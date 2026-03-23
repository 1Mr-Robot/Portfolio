FROM python:3.11-slim

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar dependencias PRIMERO
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Copiar el resto del proyecto
COPY . .

# 4. Exponer el puerto
EXPOSE 8000

# 5. Comando de arranque (Ejecuta migraciones y estáticos al iniciar)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn Portfolio.wsgi:application --bind 0.0.0.0:8000