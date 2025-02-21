run:
	docker compose -f ./docker/local/docker-compose.yml down --remove-orphans
	docker compose -f ./docker/local/docker-compose.yml up --build	
clear:
	find . -type d -name '__pycache__' -exec rm -rf {} +