#!/bin/bash
source /opt/djangoenv/bin/activate

APP_PORT=${PORT:-8080}

cd /app/

# Run migrations
/opt/djangoenv/bin/python manage.py migrate

/opt/djangoenv/bin/gunicorn --worker-tmp-dir /dev/shm djangodocker.wsgi:application \
--bind "0.0.0.0:${APP_PORT}"