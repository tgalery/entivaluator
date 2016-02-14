import codecs
try:
    import cPickle as pickle
except ImportError:
    import pickle

import logging

logger = logging.getLogger("entivaluator")


# resource = realpath(__file__).rsplit("/utils")[0] + "/resources/wiki_title_to_id.pkl"
def get_wiki_store(path_to_file):
    """
    A function that loads a title -> id dictionary
    :param path_to_file: str: path to pkl file
    :return dict:
    """

    logger.info("Loading Wiki Id map from %s", path_to_file)
    with codecs.open(path_to_file, "r") as in_file:
        return pickle.load(in_file)
