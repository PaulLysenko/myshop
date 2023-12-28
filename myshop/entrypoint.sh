#!/bin/sh

# check for postgres
echo "\n"
echo "WEB: Postgres check before Django staring..."
while ! nc -z db_postgres 5432; do
  echo "WEB: Waiting for postgres connection..."
  sleep 3
done
echo "WEB: Postgres started on db_postgres 5432"
echo "\n"

# start Django

echo "WEB: start Django \n"
# python manage.py flush --no-input  # clear DB

echo "WEB: Start migration process ..."
python myshop/manage.py migrate
echo "WEB: Migrations process done ..."
echo "\n"

python myshop/manage.py runserver 0.0.0.0:8000

exec "$@"
