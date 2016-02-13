.PHONY: install

help:
	@echo "install install dependencies"

install:
	apt-get install -y python-librdf
	pip install -r requirements.txt