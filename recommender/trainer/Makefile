ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
CODE = app

env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.template .env

install-reqs: ##@Dependencies Install requirements
	python3 -m pip install -r requirements.txt

cli:  ##@Application Run cli command
	python3 app/main.py $(args)

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist
