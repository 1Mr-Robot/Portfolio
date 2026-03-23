FROM python:3.11

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema (necesarias para MySQL)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# Copia archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto
EXPOSE 8000

# Comando de arranque
CMD ["gunicorn", "Portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]