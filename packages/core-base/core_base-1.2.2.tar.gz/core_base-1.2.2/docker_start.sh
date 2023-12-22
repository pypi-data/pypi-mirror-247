#!/bin/bash
# python manage.py makemigrations
# python manage.py migrate
# python manage.py init -y
#gunicorn -c gunicorn_conf.py sobase.asgi:sobase
uvicorn sobase.asgi:application --port 5100 --host 0.0.0.0 --workers 4
