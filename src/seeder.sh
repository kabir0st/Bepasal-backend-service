#!/bin/sh
rm db.*
rm media/ -r 
python3 manage.py makemigrations users tenants oms ecommerce
python3 manage.py flush --no-input
python3 manage.py migrate
python3 f_seeder.py
python3 manage.py populate_db
python3 manage.py runserver
