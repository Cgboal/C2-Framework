#!/bin/sh
/bin/sleep 10;
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('$DJANGO_ADMIN_USER', 'admin@example.com', '$DJANGO_ADMIN_PASS')" | /venv/bin/python manage.py shell
/venv/bin/python manage.py collectmodules
/venv/bin/uwsgi --http-auto-chunked --http-keepalive