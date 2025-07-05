SHELL = /bin/bash

.PHONY: help up down build freeze bash migrations migrate pytest superuser-dev superuser-prod admin pgadmin

.DEFAULT_GOAL := help


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'


# Docker commands
up:  ## Start containers
	docker compose -f docker-compose.yml up -d


down:  ## Remove containers
	docker compose -f docker-compose.yml down


build:  ## Build image
	docker compose -f docker-compose.yml build


freeze:  ## Run pip freeze (requirements.txt)
	pip freeze > requirements.txt


bash:
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


superuser-dev:
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py createsuperuser"


superuser-prod:
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yml run --rm -it -v $(PWD):/app web /bin/bash -c \
	"cd jbl_chat && python manage.py createsuperuser"


admin:  ## Open Django admin page
	open http://localhost:8000/admin


pgadmin:  ## Open pgadmin
	open http://localhost:8082
