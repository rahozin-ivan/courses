#!/usr/bin/env bash
# TODO write wait-for.sh script
echo -e "Wait for databases\n"
POSTGRES_TCP=$(echo "$DATABASE_URL" | sed 's/^postgres/tcp/')
dockerize -wait "$POSTGRES_TCP" -timeout 20s

if [[ "$1" = "test" ]]; then
    echo -e "Running tests\n"
    ./manage.py test

elif [[ "$1" = "worker" ]]; then
    echo -e "Running worker\n"
    celery -A conf worker --loglevel=info

elif [[ "$1" = "flower" ]]; then
    echo -e "Running flower\n"
    celery -A conf flower

elif [[ "$1" = "beat" ]]; then
    echo -e "Running beat\n"
    celery -A conf beat --loglevel=info

else
    echo -e "Collecting static assets\n"
    ./manage.py collectstatic --noinput --verbosity 0

    echo -e "Migrating database\n"
    ./manage.py migrate

    echo -e "Starting server\n"
    gunicorn --bind 0.0.0.0:8000 conf.wsgi
fi
