# Docker Deployment Guide

This guide covers both development and production Docker setups for your Django application.

## Development Environment

### Prerequisites
- Docker
- Docker Compose
- `.env` file with required environment variables

### Development Setup

The development environment uses Django's built-in development server and enables hot-reloading for faster development.

#### Configuration Files

**docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - mynetwork

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - mynetwork

volumes:
  postgres_data:

networks:
  mynetwork:
    driver: bridge
```

**Dockerfile**
```dockerfile
FROM python:3.13-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Running Development Environment

1. Create a `.env` file in the project root:
```bash
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Access the application at `http://localhost:8000`

### Development Features
- **Hot-reloading**: Code changes are reflected immediately
- **Volume mounting**: Local code is mounted into the container
- **Development server**: Uses Django's `runserver` command
- **Easy debugging**: Direct access to logs and Django debug toolbar

### Common Development Commands

```bash
# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

---

## Production Environment

### Prerequisites
- Docker
- Docker Compose
- `.env.prod` file with production environment variables
- Nginx configuration files in `./nginx/conf.d/`

### Production Setup

The production environment uses Gunicorn as the WSGI server and Nginx as a reverse proxy for better performance and security.

#### Configuration Files

**Dockerfile**
```dockerfile
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

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

**docker-compose.yml (Option 1: HTTP Port Binding)**
```yaml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env.prod
    restart: always

  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    env_file:
      - .env.prod
    depends_on:
      - db
    restart: always

  nginx:
    image: nginx:stable-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - static_volume:/app/static
      - media_volume:/app/media
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**docker-compose.yml (Option 2: Unix Socket)**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    networks:
      - mynetwork
    restart: always

  web:
    build: .
    command: gunicorn myproject.wsgi:application --bind unix:/run/gunicorn.sock --workers 3
    env_file:
      - .env.prod
    volumes:
      - static_volume:/app/static
    depends_on:
      - db
    networks:
      - mynetwork
    restart: always

  nginx:
    image: nginx:stable-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - static_volume:/app/static
      - /run/gunicorn.sock:/run/gunicorn.sock
    depends_on:
      - web
    networks:
      - mynetwork
    restart: always

volumes:
  postgres_data:
  static_volume:

networks:
  mynetwork:
    driver: bridge
```

### Nginx Configuration

Create `./nginx/conf.d/default.conf`:

**For HTTP Port Binding (Option 1):**
```nginx
upstream web {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://web;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

**For Unix Socket (Option 2):**
```nginx
upstream web {
    server unix:/run/gunicorn.sock;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://web;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/static/;
    }
}
```

### Running Production Environment

1. Create `.env.prod` file:
```bash
# Django settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=prod_db
DB_USER=prod_user
DB_PASSWORD=strong_password
DB_HOST=db
DB_PORT=5432

# PostgreSQL
POSTGRES_DB=prod_db
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=strong_password
```

2. Build and start the containers:
```bash
docker-compose -f docker-compose.yml up --build -d
```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Access the application at `http://yourdomain.com`

### Production Features
- **Gunicorn**: Production-grade WSGI server with multiple workers
- **Nginx**: Reverse proxy for static files and load balancing
- **Auto-restart**: Containers automatically restart on failure
- **Static files**: Collected and served efficiently via Nginx
- **Media files**: Persistent storage for user uploads
- **Database persistence**: PostgreSQL data stored in named volumes

### Common Production Commands

```bash
# View logs
docker-compose logs -f web
docker-compose logs -f nginx

# Restart services
docker-compose restart web
docker-compose restart nginx

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Scale workers
docker-compose up -d --scale web=5

# Execute management commands
docker-compose exec web python manage.py <command>
```

### Security Recommendations

1. **Environment Variables**: Never commit `.env.prod` to version control
2. **SECRET_KEY**: Generate a strong, unique secret key for production
3. **DEBUG**: Always set `DEBUG=False` in production
4. **ALLOWED_HOSTS**: Specify exact domains
5. **SSL/TLS**: Configure Nginx with Let's Encrypt for HTTPS
6. **Database**: Use strong passwords and restrict access
7. **Firewall**: Configure firewall rules to allow only necessary ports

### Monitoring and Maintenance

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats

# Backup database
docker-compose exec db pg_dump -U $DB_USER $DB_NAME > backup.sql

# Restore database
docker-compose exec -T db psql -U $DB_USER $DB_NAME < backup.sql
```

---

## Differences: Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Server | Django runserver | Gunicorn |
| Workers | Single-threaded | Multiple workers |
| Reverse Proxy | None | Nginx |
| Code Mounting | Live volume mount | Copied into image |
| Static Files | Served by Django | Served by Nginx |
| Auto-reload | Enabled | Disabled |
| Debug Mode | Enabled | Disabled |
| Container Restart | Manual | Automatic |

---

## Troubleshooting

### Development Issues

**Container won't start:**
```bash
docker-compose down
docker-compose up --build
```

**Database connection errors:**
- Check `.env` file has correct credentials
- Ensure database service is running: `docker-compose ps`

### Production Issues

**502 Bad Gateway:**
- Check Gunicorn is running: `docker-compose logs web`
- Verify Nginx configuration: `docker-compose exec nginx nginx -t`

**Static files not loading:**
- Run collectstatic: `docker-compose exec web python manage.py collectstatic --noinput`
- Check Nginx volume mappings

**Permission errors:**
- Ensure proper file permissions on mounted volumes
- Check container user permissions

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
