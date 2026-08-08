#!/bin/bash
set -e

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "RUN_MIGRATIONS=true -> ejecutando migraciones..."
    alembic upgrade head
else
    echo "RUN_MIGRATIONS no está en true, se omiten migraciones."
fi

exec "$@"