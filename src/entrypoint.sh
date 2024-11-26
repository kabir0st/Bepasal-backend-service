#!/bin/bash

echo "Postgres is up - executing command"

# Check if any migrations are unapplied
echo "Checking for unapplied migrations..."
python3 wait_for_db.py
UNAPPLIED_MIGRATIONS=$(python3 manage.py showmigrations --plan | grep '\[ \]' | wc -l)

if [ "$UNAPPLIED_MIGRATIONS" -gt "0" ]; then
    echo "Unapplied migrations detected, running migrations and seeders..."
    rm db.*
    rm media/ -r 
    python3 manage.py sqlflush
    python3 manage.py makemigrations users tenants system ecommerce
    python3 manage.py flush --no-input
    python3 manage.py migrate
    python3 f_seeder.py
    python3 manage.py populate_system
    python3 manage.py populate_site    
else
echo "Unapplied migrations detected, running migrations and seeders..."
    python3 manage.py makemigrations tenants system inventory statements transactions cafe
    python3 manage.py migrate 
    echo "All migrations are applied, skipping migration and seeding."
fi

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
exec "$@"