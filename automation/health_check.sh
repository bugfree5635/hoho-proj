#!/bin/bash

set -e

URL="http://localhost:8000/health"

echo "Checking application health..."

if curl --fail --silent "$URL" > /dev/null; then
    echo "Application is healthy."
else
    echo "Application is unhealthy."
    exit 1
fi
