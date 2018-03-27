#!/bin/sh
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('$DJANGO_ADMIN_USER', 'admin@example.com', '$DJANGO_ADMIN_PASS')" | /venv/bin/python manage.py shell
cd /code/agent/
/venv/bin/python setup.py bdist_wheel
cd /code/
/venv/bin/uwsgi --http-auto-chunked --http-keepalive