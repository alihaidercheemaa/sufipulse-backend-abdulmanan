#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -U sufi_pulse_user -d sufi_pulse_db; do
  sleep 2
done

echo "PostgreSQL is ready, importing dump..."

# Restore the dump file
pg_restore --username=sufi_pulse_user --dbname=sufi_pulse_db --clean --no-owner --no-privileges /docker-entrypoint-initdb.d/2-data.dump

echo "Dump import completed!"