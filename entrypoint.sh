#!/bin/sh

sleep 2

python manage.py migrate
python manage.py migrate parsing

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email $DJANGO_SUPERUSER_EMAIL
fi

python manage.py collectstatic --noinput
gunicorn my_parser.wsgi:application --bind 0.0.0.0:8000

exec "$@"