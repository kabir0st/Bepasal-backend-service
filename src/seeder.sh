#!/bin/sh
rm db.*
rm media/ -r 
python3 manage.py sqlflush
python3 manage.py makemigrations users tenants system ecommerce
python3 manage.py flush --no-input
python3 manage.py migrate
python3 f_seeder.py
python3 manage.py populate_system
python3 manage.py populate_site
