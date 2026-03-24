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

# Dar permisos al entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Usar entrypoint
ENTRYPOINT ["/entrypoint.sh"]