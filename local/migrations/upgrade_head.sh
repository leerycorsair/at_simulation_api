#!/bin/bash

# Set environment variables
cd .. 
set -a && source .env

# Run upgrade head script
cd ../migrations || exit
set +a && bash ./upgrade_head.sh
