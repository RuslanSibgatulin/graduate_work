## ----------------------------------------------------------------------
## The purpose of this Makefile is to manage PostgreSQL tests.
## ----------------------------------------------------------------------
compose_files=-f docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Launching the project infrastructure.
		docker-compose $(compose_files) up -d --build
stop:  ## Stop project.
		docker-compose $(compose_files) down

db-shell:  ## Open psql shell. Use database db_test
		docker exec -it postgres psql -Utest -ddb_test

full-test:  ## Run full tests over pytest
		pytest tests/ -vvs --durations=0

read-tests:  ## Run read tests only over pytest
		pytest tests/ -vvs -k 'not insert' --durations=0