#!/bin/sh
kill -15 $(cat /var/run/uwsgi.pid);
/bin/sleep 1;
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py migrate --noinput
/venv/bin/python manage.py collectmodules
/venv/bin/uwsgi --http-auto-chunked --http-keepalive