.PHONY: install

help:
	@echo "install dependencies"

install:
	apt-get install -y git python-librdf maven
	pip install -r requirements.txt
	cd dexter-eval && git submodule init && git submodule update && mvn clean assembly:single

