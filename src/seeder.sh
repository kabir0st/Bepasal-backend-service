#!/bin/sh
rm db.*
rm media/ -r 
python3 manage.py makemigrations tenants users
# python3 manage.py flush
python3 manage.py migrate
python3 f_seeder.py