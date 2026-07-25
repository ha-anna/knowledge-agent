.DEFAULT_GOAL := help

.PHONY: help compile sync install dev format lint test clean \
        docker-build docker-up docker-down docker-logs docker-rebuild

help:
	@echo ""
	@echo "Knowledge Agent"
	@echo "=============================="
	@echo "Dependencies:"
	@echo "  make compile      Compile requirements.in"
	@echo "  make sync         Sync virtual environment"
	@echo "  make install      Compile + sync"
	@echo ""
	@echo "Development:"
	@echo "  make dev          Run FastAPI"
	@echo "  make format       Format code"
	@echo "  make lint         Run Ruff"
	@echo "  make test         Run tests"
	@echo "  make clean        Remove caches"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build"
	@echo "  make docker-up"
	@echo "  make docker-down"
	@echo "  make docker-logs"
	@echo "  make docker-rebuild"

compile:
	pip-compile requirements.in

sync:
	pip-sync requirements.txt

install: compile sync

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

format:
	ruff format .

lint:
	ruff check .

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-rebuild:
	docker compose down
	docker compose build --no-cache
	docker compose up