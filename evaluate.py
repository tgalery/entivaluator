"""Entity Linker Evaluator

Usage: evaluate.py <entity-linker> <gs-file-path> <base-endpoint> <output-file>
"""
import codecs
import logging
import sys

from docopt import docopt

from annotators.spotlight import get_entities, format_data
from utils.text import parse_gs_line

SUPPORTED_LINKERS = {"spotlight"}
logger = logging.getLogger("entivaluator")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel('INFO')

def die(msg):
    logger.info(msg)
    sys.exit(1)


def main(args):
    ent_linker_name = args["<entity-linker>"].lower()
    base_endpoint = args["<base-endpoint>"].lower()
    infile = None
    outfile = None
    if ent_linker_name not in SUPPORTED_LINKERS:
        die(ent_linker_name + " is not a supported entity linking system. Exiting.")

    try:
        infile = codecs.open(args["<gs-file-path>"], "r", encoding="utf8")
        outfile = codecs.open(args["<output-file>"], "w", encoding="utf8")
    except Exception as ex:
        logger.exception("An exception occured, %s", ex)
        die("Could not read from gold standard file or not write to output file")
    if infile and outfile:
        logger.info("Starting Entity Linking benchmark")
        for doc in infile:
            doc_data = parse_gs_line(doc)
            if ent_linker_name == "spotlight":
                doc_id = doc_data["docId"]
                doc_text = doc_data["text"]
                logger.info("Processing entities for document %s . First chars are %s", doc_id, doc_text[:10])
                entities = get_entities(base_endpoint, doc_data["text"])
                logger.info("Retrieved %d entitines", len(entities))
                out_data = format_data(entities)
                for data_row in out_data:
                    if data_row:
                        data_row.insert(0, doc_data["docId"])
                        logger.info("Retrieved entity : %s", data_row[5 ])
                        data_line = u"\t".join(data_row) + u"\n"
                        outfile.write(data_line)
        infile.close()
        outfile.close()






if __name__ == '__main__':
    args = docopt(__doc__, argv=sys.argv[1:])
    main(args)
