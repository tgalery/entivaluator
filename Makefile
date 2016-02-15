.PHONY: data deps clean install

help:
	@echo "deps - installs dependencies"
	@echo "data - downloads data"
	@echo "clean - removes dowloaded files"
	@echo "install - installs dependencies and downloads data"

data:
	cd resources && tar -xzvf iitb-sorted.json.tgz && cd ..
	wget -O resources/wiki_title_to_id.pkl.tgz -v https://googledrive.com/host/0B7wSO4JK9zbFanFTbUJ4WFROYms && cd resources && tar -xzvf wiki_title_to_id.pkl.tgz && cd ..

clean:
	rm resources/iitb-sorted.json
	rm resources/wiki_title_to_id.pkl
	cd dexter-eval && mvn clean && cd ..
	rm -r -f output

deps:
	sudo apt-get install -y git python-librdf maven
	sudo pip install -r requirements.txt
	git submodule update --init --recursive && cd dexter-eval && mvn clean package assembly:single && cd ..
	mkdir -p output

install: deps data
