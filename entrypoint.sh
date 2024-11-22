#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/
/opt/djangoenv/bin/gunicorn --worker-tmp-dir /dev/shm djangodocker.wsgi:application
--bind "0.0.0.0:${APP_PORT}"