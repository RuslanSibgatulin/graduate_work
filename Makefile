## ----------------------------------------------------------------------
## Makefile.
## ----------------------------------------------------------------------
compose = -f docker-compose-etl.yaml


help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start: ## Start 
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose} up -d --build --force-recreate

stop: ## Stop
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose} down

init:  ## First and full initialization.
		# TODO: Init here

restart: stop start
		