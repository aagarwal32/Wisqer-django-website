#!/bin/bash
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"walkdeplankz@gmail.com"}
cd /app/

/opt/djangoenv/bin/python manage.py migrate --noinput
/opt/djangoenv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true