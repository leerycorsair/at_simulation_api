#!/bin/bash

set -eo pipefail

if [ -z "$1" ]; then
    echo "Error: Please provide a revision message"
    echo "Usage: $0 \"Your revision message\""
    exit 1
fi

# Set environment variables
cd .. 
set -a && source .env

# Run create revision script
cd ../migrations || exit
set +a && ./create_revision.sh "$1"
