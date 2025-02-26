
include docker/local/.env
run:
	bash -c "poetry run python application.py"

clear:
	find . -type d -name '__pycache__' -exec rm -rf {} +

components:
	docker compose -f ./docker/local/docker-compose.yml down --remove-orphans
	docker compose -f ./docker/local/docker-compose.yml up --build -d