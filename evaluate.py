"""Entity Linker Evaluator

Usage:
    evaluate.py gen-report <entity-linker> <gs-file-path> <output-file>
    evaluate.py with-dexter-eval <entity-linker> <gs-file-path> <output-file>
    evaluate.py all-with-dexter-eval <entity-linker>
    evaluate.py gen-id-store <redirects-path> <page-ids-path> <output-path>

"""
import codecs
from datetime import datetime
import json
from os import path
import re
import subprocess
import sys

from docopt import docopt

from annotators.spotlight import get_entities, format_data
from utils.logger import get_logger
from utils.io import generate_title_id_map

SUPPORTED_LINKERS = {"spotlight"}
BASE_DIR = path.dirname(path.realpath(__file__))
EXP = r"(\w+\d?)\s+(\d+\.?\d+)"

logger = get_logger()


def die(msg):
    """
    A helper function to display messages and exit the interpreter.
    :param msg: str: message to display
    """
    logger.info(msg)
    sys.exit(1)


def gen_report(infile_path, outfile_path, linker_name):
    """
    A function to generate a report that can be used by dexter.
    :param infile_path: str: input gold standard
    :param outfile_path: str: output of tsv predictions
    :param linker_name: str: name of entity linker
    """

    infile = codecs.open(infile_path, "r", encoding="utf8")
    outfile = codecs.open(outfile_path, "w", encoding="utf8")
    if infile and outfile:
        logger.info("Starting Entity Linking benchmark")
        for doc in infile:
            doc_data = json.loads(doc)
            if linker_name == "spotlight":
                entities = get_entities(doc_data["text"])
                n_entities = len(entities["Resources"]) if "Resources" in entities else 0
                logger.info("Retrieved %d entities for document %s",
                            n_entities, doc_data["docId"])
                out_data = format_data(entities)
                for data_row in out_data:
                    if data_row:
                        data_row.insert(0, doc_data["docId"])
                        data_line = u"\t".join(data_row) + u"\n"
                        outfile.write(data_line)
        infile.close()
        outfile.close()


def with_dexter_eval(infile, outfile, ent_linker_name):
    """
    A function to generate a report that can be used by dexter.
    :param infile: str: input gold standard
    :param outfile: str: output of tsv predictions
    :param ent_linker_name: str: name of entity linker
    """
    gen_report(infile, outfile, ent_linker_name)
    logger.info("Running benchmarks using dexter-eval framework.")
    proc = subprocess.Popen([path.join(BASE_DIR, "dexter-eval/scripts/evaluate.sh"),
                             outfile, infile, "Mwa",
                             path.join(BASE_DIR, "dexter_macro_conf.txt")],
                            stdout=subprocess.PIPE,
                            cwd=path.join(BASE_DIR, "dexter-eval"))
    output, err = proc.communicate()
    logger.info("Finished running dexter eval. \n")
    logger.info("%s", output)
    output_tuples = re.findall(EXP, output)
    precision = output_tuples[0][1]
    recall = output_tuples[1][1]
    f1 = output_tuples[2][1]
    base_file_name = outfile.split(".tsv")[0].rsplit("/", 1)[1]
    dexter_file_path = BASE_DIR + "/output/{}_dexter_out.tsv".format(base_file_name)
    with open(dexter_file_path, "w") as dexter_out:
        logger.info("Generating dexter out tsv at %s.", dexter_file_path)
        dexter_out.write("\t".join([precision, recall, f1]) + "\n")


def main(args):
    """
    Entry point of the evaluation sysem.
    :param args: list: command line args
    """

    if args["gen-id-store"]:
        logger.info("Generating id stores at %s ", args["<output-path>"])
        _ = generate_title_id_map(args["<redirects-path>"], args["<page-ids-path>"], args["<output-path>"])
        sys.exit(0)

    ent_linker_name = args["<entity-linker>"].lower()

    # generate report
    if args["gen-report"]:
        infile = path.realpath(args["<gs-file-path>"])
        outfile = path.realpath(args["<output-file>"])
        gen_report(infile, outfile, ent_linker_name)
        logger.info("Finished generating report at %s", args["<output-file>"])
        sys.exit(0)

    if args["with-dexter-eval"]:
        infile = path.realpath(args["<gs-file-path>"])
        outfile = path.realpath(args["<output-file>"])
        with_dexter_eval(infile, outfile, ent_linker_name)

    if args["all-with-dexter-eval"]:
        timestamp = datetime.utcnow().strftime('%Y:%H:%M:%S')
        for data_path in ["resources/AQUAINT-dataset.json",
                          "resources/MSNBC-dataset.json",
                          "resources/iitb-sorted.json"]:
            out_file_name = "output/{}_{}_{}.tsv".format(
                ent_linker_name,
                data_path.split("/")[1].split("-")[0].lower(),
                timestamp)
            with_dexter_eval(
                path.realpath(data_path),
                path.realpath(out_file_name),
                ent_linker_name)


if __name__ == '__main__':
    """
    Function to pass the command line args to the main function of the module.
    """
    args = docopt(__doc__, argv=sys.argv[1:])
    main(args)
