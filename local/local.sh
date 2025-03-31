#!/bin/bash

docker network create custom-network

source .env

cd .. && poetry run python -m at_simulation_api 