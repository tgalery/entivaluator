"""Entity Linker Evaluator

Usage:
    evaluate.py gen-report <entity-linker> <gs-file-path> <output-file>
    evaluate.py with-dexter-eval <entity-linker> <gs-file-path> <output-file>

"""
import codecs
import json
import logging
from os import path
import subprocess
import sys

from docopt import docopt

from annotators.spotlight import get_entities, format_data

SUPPORTED_LINKERS = {"spotlight"}
BASE_DIR = path.dirname(path.realpath(__file__))

logger = logging.getLogger("entivaluator")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel('INFO')


def die(msg):
    """
    A helper function to display messages and exit the interpreter.
    :param msg: str: message to display
    """
    logger.info(msg)
    sys.exit(1)


def gen_report(infile, outfile, linker_name):
    """
    A function to generate a report that can be used by dexter.
    :param infile: file: input gold standard
    :param outfile file: ouput of tsv predictions
    """

    if infile and outfile:
        logger.info("Starting Entity Linking benchmark")
        for doc in infile:
            doc_data = json.loads(doc)
            if linker_name == "spotlight":
                entities = get_entities(doc_data["text"])
                logger.info("Retrieved %d entities for document %s",
                            len(entities), doc_data["docId"])
                out_data = format_data(entities)
                for data_row in out_data:
                    if data_row:
                        data_row.insert(0, doc_data["docId"])
                        data_line = u"\t".join(data_row) + u"\n"
                        outfile.write(data_line)
        infile.close()
        outfile.close()


def main(args):
    """
    Entry point of the evaluation sysem.
    :param args: list: command line args
    """

    ent_linker_name = args["<entity-linker>"].lower()
    infile = None
    outfile = None
    if ent_linker_name not in SUPPORTED_LINKERS:
        die(u"{} is not a supported entity linking system. Exiting.".format(ent_linker_name))

    try:
        infile = codecs.open(args["<gs-file-path>"], "r", encoding="utf8")
        outfile = codecs.open(args["<output-file>"], "w", encoding="utf8")
    except Exception as ex:
        logger.exception("An exception occured, %s", ex)
        die("Could not read from gold standard file or not write to output file.")
    # generate report
    if args["gen-report"]:
        gen_report(infile, outfile, ent_linker_name)
        logger.info("Finished generating report at %s", args["<output-file>"])
        sys.exit(0)

    if args["with-dexter-eval"]:
        gen_report(infile, outfile, ent_linker_name)
        logger.info("Running benchmarks using dexter-eval framework.")
        proc = subprocess.Popen([path.join(BASE_DIR, "dexter-eval/scripts/evaluate.sh"),
                                 args["<output-file>"], args["<gs-file-path>"], "Mwa",
                                 path.join(BASE_DIR, "dexter_macro_conf.txt")],
                                stdout=subprocess.PIPE,
                                cwd=path.join(BASE_DIR, "dexter-eval"))
        output, err = proc.communicate()
        logger.info("Finished running dexter eval. \\n")
        logger.info("%s", output)


if __name__ == '__main__':
    """
    Function to pass the command line args to the main function of the module.
    """
    args = docopt(__doc__, argv=sys.argv[1:])
    main(args)
