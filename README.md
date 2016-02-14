## Entivaluator

This is a command line tool to help evaluate entity linking systems using [dexter-eval](https://github.com/diegoceccarelli/dexter-eval). It basically reads the data from a gold standard file in json format, queries the endpoint of an entity linking system, and writes the output to a .tsv that dexter eval can read.

### Installation

#### Clone

Clone this repo, to begin with. Once you have it, cd into it and run `make install`.
This will do the following:

1. Install some dependencies (sudo password will be prompted, at the moment only debian systems are supported, but otherwise you can just pip install the requirements and use `make data`)
2. Pull the stable version of `dexter-eval` and build it.
3. Download a pre-processed dictionary of wiki titles -> ids (you can do this by issuing `make data`)
4. Create an `output` folder where some of the output will be stored.

### Usage

#### Specifying gold standards and output paths from the command line

From the root of this repo, you can use a command with the following syntax:

*  `python evaluate.py with-dexter-eval <entity-linker> <gold-standard-json-file> <output-file.tsv>`

In this command, the following holds:

* `<entity-linker>` the name of the entity linking system you are testing. At the moment only `spotlight` is supported.
* `<gold-standard-json-file>` the gold standard file that contains the text and entities, i.e. `resources.iitb-sorted.json`
* `<output-file.tsv>` this the path to a filename which the tool will create. Make sure it ends with `.tsv` otherwise dexter eval might not parse it.


This will generate a tsv file which in turn is feed into dexter-eval's evaluation module.
You will see some scores printed on the screen.
Also, a resulting file with a `dexter_out.tsv` suffix should appear in the output folder.
This is a simple `tsv` file with precision, recall and f1 scores.

Note that `entivaluator` assumes the configuration specified in `dexter_macro_conf.txt`. 
Moreover, the metric chosen is the weak mention annotation or `Mwa`, that is:
two annotations are considered to be the same, if the surface forms overall and they refer to the same entity.
If you want to chose a different metric or measure, you might try to use [dexter-eval](https://github.com/diegoceccarelli/dexter-eval) as a CLI tool against the `.tsv` file produced by the step above manually.


#### Bundled Data

This repo comes with the `iitb`, `ACQUAINT` and `MSNBC` data sets.
If you want to evaluate your entity linker against all of those, you can run:

`python evaluate.py all-with-dexter-eval <entity-linker>`

This command basically loops over each dataset (in `resources`),
creates a datastamp and uses that and the name of the entity linker to create `.tsv` files in the `output` folder.

### Contributions

It would be nice to (i) have tests, (ii) have python 3 support, (iii) support more entity linking systems, and (iv) support more datasets. So why don't you ?

