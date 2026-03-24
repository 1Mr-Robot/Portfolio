#!/bin/sh

set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking superuser..."

python << END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portfolio.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv('SUPERUSER_USERNAME')
email = os.getenv('SUPERUSER_EMAIL')
password = os.getenv('SUPERUSER_PASSWORD')

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created")
else:
    print("Superuser already exists or not defined")
END

echo "Starting server..."
exec gunicorn Portfolio.wsgi:application --bind 0.0.0.0:8000