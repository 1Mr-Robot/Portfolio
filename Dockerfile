FROM python:3.11.15-alpine3.23

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    mariadb-dev \
    pkgconfig

COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    #python manage.py runserver 0.0.0.0:8000
    gunicorn Portfolio.wsgi:application --bind 0.0.0.0:8000