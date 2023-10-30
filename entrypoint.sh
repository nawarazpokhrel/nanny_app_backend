#!/bin/sh

# Activate the virtual environment
source /home/app/webapp/venv/bin/activate

# Start Django development server
echo "Starting server"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8002
python manage.py createadmin
