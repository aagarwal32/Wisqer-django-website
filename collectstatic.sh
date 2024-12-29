#!/bin/bash
cd /app/
/opt/djangoenv/bin/python manage.py collectstatic --noinput
