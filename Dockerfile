FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ARG SECRET_KEY
ARG SERVER
ARG DEBUG
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV SECRET_KEY=${SECRET_KEY}
ENV SERVER=${SERVER}
ENV DEBUG=${DEBUG}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

# RUN python3 manage.py migrate --no-input
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "application.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]