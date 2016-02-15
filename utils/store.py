import codecs
import json
try:
    import cPickle as pickle
except ImportError:
    import pickle

from utils.logger import get_logger

logger = get_logger()


# resource = realpath(__file__).rsplit("/utils")[0] + "/resources/wiki_title_to_id.pkl"
def get_wiki_store(path_to_file):
    """
    A function that loads a title -> id dictionary
    :param path_to_file: str: path to pkl file
    :return dict:
    """

    logger.info("Loading Wiki Id map from %s", path_to_file)
    in_file = codecs.open(path_to_file)
    if path_to_file.endswith(".pkl"):
        return pickle.load(in_file)
    elif path_to_file.endswith(".json"):
        return json.load(in_file)
