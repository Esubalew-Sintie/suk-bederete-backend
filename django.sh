#!/bin/bash

echo "creating migration"
python manage.py makemigrations
echo "==============================="

echo "migrating"
python manage.py migrate
echo "==============================="

echo "running server"
python manage.py runserver 0.0.0.0:8000
