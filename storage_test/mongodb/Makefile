## ----------------------------------------------------------------------
## The purpose of this Makefile is to manage MongoDB tests.
## ----------------------------------------------------------------------
compose_files=-f mongo-docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Launching the project infrastructure.
		docker-compose $(compose_files) up -d --build
stop:  ## Stop project.
		docker-compose $(compose_files) down

clear:  ## Clear Mongo cache
		sudo rm -R /tmp/mongo_cluster/

status:  ## Get docker containers status
		docker-compose $(compose_files) ps

init:  ## Configure Mongo cluster and create database UGC_data
		./rs-init.sh
		sleep 5
		./db-init.sh

full-test:  ## Run full tests
		pytest ./tests/views_test.py -vvs --durations=0

read-tests:  ## Run read only tests
		pytest ./tests/views_test.py -v -k 'not insert' --durations=0

