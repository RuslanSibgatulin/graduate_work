## ----------------------------------------------------------------------
## Makefile.
## ----------------------------------------------------------------------
compose = -f docker-compose.yaml


help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

env:  ##@Environment Create .env files from examples
		 @$(eval SHELL:=/bin/bash)
		 @for file in $$(find docker/envs -type f -name "*.example"); do cp $$file $${file%.example}.env; done;

start: ## Start 
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose} up -d --build --force-recreate

stop: ## Stop
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose} down

init:  ## Initialization.
		# TODO: Init here

lint:
		isort etl/ recommendation_app/ recommender/
		flake8 etl/ recommendation_app/ recommender/ --show-source

restart: stop start
		docker restart nginx

		