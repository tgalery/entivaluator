from annotators.conf import TITLE_TO_ID, ENDPOINTS
from utils.html import check_json_response, post_request
from utils.text import remove_illegal_chars
from utils.store import get_wiki_store
from utils.logger import get_logger


logger = get_logger()
wiki_id_db = get_wiki_store(TITLE_TO_ID["spotlight"])


def get_entities(text, conf=0.45):
    """
    A function to get annotations.
    :param text: str: text to annotate
    :param conf: float: confidence
    :return: list
    """

    payload = {"text": remove_illegal_chars(text), "confidence": conf}
    spotlight_headers = {'accept': 'application/json',
                         'content-type': 'application/x-www-form-urlencoded'}

    response = post_request(ENDPOINTS["spotlight"], payload, spotlight_headers)
    return check_json_response(response)


def format_data(json_response):
    """
    A function for formatting output data in a dexter-eval format.
    :param text: str: text to annotate
    :return: list
    """
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
                output.append([surface_form, unicode(start), unicode(end),
                               wiki_id, title, score])
            except Exception:
                logger.warning("Could not find wikipedia id for title: %s", title)
                continue
    return output
