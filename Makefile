SHELL = /bin/bash

.PHONY: help up down build freeze bash migrations migrate pytest superuser-dev \
        superuser-prod seed-dev seed-prod flush-dev admin pgadmin web setup nuke

.DEFAULT_GOAL := help


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'


up:  ## Start containers
	docker compose -f docker-compose.yml up -d


down:  ## Remove containers
	docker compose -f docker-compose.yml down


build:  ## Build image
	docker compose -f docker-compose.yml build


freeze:  ## Run pip freeze (requirements.txt)
	pip freeze > requirements.txt


bash:  ## Open a bash shell in web service
	docker compose -f docker-compose.yml run --rm -it web bash -c "cd jbl_chat && exec bash"


migrations:  ## Run migrations (development)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py makemigrations"


migrate:  ## Run migrate (development + production)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py migrate"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py migrate"


pytest:  ## Run pytest
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"python -m pytest"


cov:  ## Run tests and make coverage report
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"pytest --cov --cov-report html:coverage/html" \
	&& open coverage/html/index.html


superuser-dev:  ## Create a superuser in development environment
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py createsuperuser"


superuser-prod:  ## Create a superuser in production environment
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py createsuperuser"


seed-dev:  ## fill db-development with seed data
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py seed"


seed-prod:  ## fill db-production with seed data
	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py seed"


flush-dev:
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py flush"


admin:  ## Open Django admin page
	open http://localhost:8000/admin


pgadmin:  ## Open pgadmin
	open http://localhost:8082


web:  ## Open web
	open http://localhost:8000


setup:  ## Setup project resources
	@if [ ! -f .env ]; then cp .env.example .env && echo ".env created"; else echo ".env already exists"; fi
	make build
	docker compose -f docker-compose.yml up -d db-development db-testing db-production pgadmin
	@echo "Waiting for PostgreSQL to be ready..."
	@until docker compose -f docker-compose.yml exec -T db-development sh -c 'pg_isready -U postgres -d db-development | grep "accepting connections" > /dev/null'; do \
		echo "Still waiting..."; \
		sleep 1; \
	done
	docker compose -f docker-compose.yml up -d web
	sleep 5
	make migrate
	make seed-dev
	make web


nuke:  ## Delete project resources (non-reversible)
	make down
	rm -rf .env
	rm -rf compose/db_development/db_development_data/
	rm -rf compose/db_production/db_production_data/
	rm -rf compose/db_testing/db_testing_data/
	rm -rf compose/pgadmin/pgadmin_data/
