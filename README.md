## Entivaluator

This is a command line tool to help evaluate entity linking systems using [dexter-eval](https://github.com/diegoceccarelli/dexter-eval). It basically reads the data from a gold standard file in json format, queries the endpoint of an entity linking system, and writes the output to a .tsv that dexter eval can read.

### Installation

#### Clone

Clone this repo, to begin with. You also need to clone and build [dexter-eval](https://github.com/diegoceccarelli/dexter-eval) so this has any use. Go ahead and do that.

#### Libraries

The package comes with a `requirements.txt` file, so a simple `pip install -r requirements.txt` would do. If you install outside the python system libraries, make sure that the libs are added to the python path.

#### Data

In order to evaluate entity linking systems, you need to convert dbpedia/wikipedia titles to their corresponding numerical ids. I have prepared a json file with the titles as keys and the numerical ids as values.  The program expects this file to be in the `resources` folder. To download it, you need to run:

1. `cd resources`
2. `wget -O wiki_title_to_id.json.tgz -v https://googledrive.com/host/0B7wSO4JK9zbFeHRTYmJGa2ZjTU0`
3. `tar -xzvf wiki_title_to_id.json.tgz`

Note that the program presupposes the file to be named `wiki_title_to_id.json`, so make sure that's the correct filename of the json file. Dexter-eval comes with the iitb dataset, you can unpack that file and use it, but if you want to download a version of that, you can simply unpack the version that comes in the resources folder.

* `tar -xzvf iitb-sorted.json.tgz`

### Usage

From the root of this repo, you can use a command with the following syntax:

*  `python evaluate.py <entity-linker> <gold-standard-json-file> <entity-extraction-endpoint> <output-file.tsv>`

In this command, the following holds:

* `<entity-linker>` the name of the entity linking system you are testing. At the moment only `spotlight` is supported.
* `<gold-standard-json-file>` the gold standard file that contains the text and entities, i.e. `resources.iitb-sorted.json`
* `<entity-extraction-endpoint>` the endpoint of the service that extracts entities. If you are using DBpedia Spotlight locally, this is probably `http://localhost:2222/rest/annotate`
* `<output-file.tsv>` this the path to a filename which the tool will create. Make sure it ends with `.tsv` otherwise dexter eval might not parse it.


Once the output file is generated and assuming you have dexter eval installed and compiled. You can run comparison for your system by doing:

* `<path-to-dexter-eval>/scripts/evaluate.sh <output-file.tsv> <gold-standard-json-file> <Metric> <Config>`

Note that the `<Metric>` and `<Config>` are specified in the [dexter-eval documentation](https://github.com/diegoceccarelli/dexter-eval), so I would refer to that.

### Contributions

It would be nice to (i) have tests, (ii) have python 3 support, (iii) support more entity linking systems, and (iv) support more datasets. So if you feel like contributing in any of those areas it would be much appreciated.

