ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

CODE = app

env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.template .env

install-reqs: ##@Dependencies Install requirements
	python3 -m pip install -r requirements.txt -r requirements.dev.txt --no-dependencies 

format:  ##@Code Reformat code with isort and black
	python3 -m isort $(CODE)
	python3 -m black $(CODE)

run:  ##@Application Run application server
	cd app && python3 main.py 

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist
