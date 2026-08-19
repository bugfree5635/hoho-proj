#!/bin/bash

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/company_$TIMESTAMP.dump"

mkdir -p "$BACKUP_DIR"

echo "Creating PostgreSQL backup..."

docker compose -f docker/docker-compose.yml exec -T postgres \
    pg_dump \
    -U admin \
    -Fc \
    company > "$BACKUP_FILE"

echo "Backup created:"
echo "$BACKUP_FILE"
