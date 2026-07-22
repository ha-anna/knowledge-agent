.PHONY: help compile sync install dev clean

help:
	@echo "Available commands:"
	@echo "  make compile"
	@echo "  make sync"
	@echo "  make install"
	@echo "  make dev"
	@echo "  make clean"

compile:
	pip-compile requirements.in

sync:
	pip-sync requirements.txt

install: compile sync

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f
