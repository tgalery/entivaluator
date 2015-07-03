import logging
from os.path import realpath

from utils.html import check_json_response, post_request
from utils.text import int2utf8, remove_illegal_chars
from utils.store import get_wiki_store

db_dir = realpath(__file__).rsplit("/annotators")[0] + "/resources/wiki_title_to_id"

logger = logging.getLogger("entivaluator")

wiki_id_db = get_wiki_store()

def get_entities(endpoint, text, conf=0.5, support=5):
    payload = {"text": remove_illegal_chars(text), "confidence": conf, "support": support}
    spotlight_headers = {'accept': 'application/json',
                         'content-type': 'application/x-www-form-urlencoded'}

    response = post_request(endpoint, payload, spotlight_headers)
    return check_json_response(response)


def format_data(json_response):
    output = []
    key = "Resources"
    if json_response and key in json_response and json_response[key]:
        entities = json_response["Resources"]
        for ent in entities:
            try:
                surface_form = ent["@surfaceForm"]
                title = ent["@URI"].rsplit("resource/", 1)[1]
                wiki_id = wiki_id_db[title]
                score = ent["@percentageOfSecondRank"]
                start = int(ent["@offset"])
                end = start + len(surface_form)
                output.append([surface_form, int2utf8(start), int2utf8(end), wiki_id, title, score])
            except Exception as ex:
                logger.warning("Exception %s", ex)
                continue
    return output