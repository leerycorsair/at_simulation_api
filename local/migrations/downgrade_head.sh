#!/bin/bash

# Set environment variables
cd .. 
set -a && source .env

# Run downgrade head script
cd ../migrations || exit
set +a && bash ./downgrade_head.sh
