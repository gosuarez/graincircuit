#!/bin/sh

set -o errexit
set -o nounset

# Wait for PostgreSQL to be ready
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

    timeout=30
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
        timeout=$((timeout - 1))
        if [ $timeout -le 0 ]; then
            echo "PostgreSQL did not start in time. Exiting."
            exit 1
        fi
    done

    echo "PostgreSQL is available at $DB_HOST:$DB_PORT"
fi

# Run the command passed to the container
exec "$@"