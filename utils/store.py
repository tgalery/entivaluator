import codecs
import json
import logging
from os.path import realpath

logger = logging.getLogger("entivaluator")

def get_wiki_store():
    resource = realpath(__file__).rsplit("/utils")[0] + "/resources/wiki_title_to_id.json"
    logger.info("Loading Wiki Id map")
    wiki_file = codecs.open(resource, "r", "utf8")
    wiki_store = json.load(wiki_file)
    wiki_file.close()
    logger.info("Finishing loading Wiki Id map")
    return wiki_store
