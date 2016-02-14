.PHONY: data deps clean install

help:
	@echo "deps - installs dependencies"
	@echo "data - downloads data"
	@echo "clean - removes dowloaded files"
	@echo "install - installs dependencies and downloads data"

data:
	cd resources && tar -xzvf iitb-sorted.json.tgz && cd ..
	wget -O resources/wiki_title_to_id.pkl.tgz -v https://googledrive.com/host/0B7wSO4JK9zbFakRhenVxZUxkZk0 && cd resources && tar -xzvf wiki_title_to_id.pkl.tgz && cd ..

clean:
	rm resources/iitb-sorted.json
	rm resources/wiki_title_to_id.pkl
	cd dexter-eval && mvn clean && cd ..

deps:
	sudo apt-get install -y git python-librdf maven
	sudo pip install -r requirements.txt
	cd dexter-eval && git submodule init && git submodule update && mvn clean assembly:single
	mkdir -p output

install: deps data
