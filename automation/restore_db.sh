#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Usage:"
    echo "./scripts/restore_db.sh backups/company_YYYYMMDD_HHMMSS.dump"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found:"
    echo "$BACKUP_FILE"
    exit 1
fi

echo "Restoring database from:"
echo "$BACKUP_FILE"

docker compose -f docker/docker-compose.yml exec -T postgres \
    pg_restore \
    -U admin \
    -d company \
    --clean \
    --if-exists \
    < "$BACKUP_FILE"

echo "Database restore completed."
