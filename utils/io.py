import codecs
try:
    import cPickle as pickle
except ImportError:
    import pickle

import bz2file
import gzip
import RDF

from utils.logger import get_logger

DBPEDIA_RES_URI = "http://dbpedia.org/resource/"

logger = get_logger()


def open_file(file_path):
    """
    A function to open files in different extensions.
    :param file_path: str: path to input file
    :return: function
    """
    open_fn = codecs.open
    if file_path.endswith(".bz2"):
        open_fn = bz2file.open
    elif file_path.endswith(".gz"):
        open_fn = gzip.open
    return open_fn


def get_rdf_parser(file_path):
    """
    A function that generates a parser depending on the extension.
    :param file_path: str: path to rdf file
    :return: RDF.Parser
    """
    if ".ttl" in file_path:
        return RDF.TurtleParser()

    elif ".nt" in file_path:
        return RDF.NTriplesParser()
    else:
        raise ValueError("RDF parser for extension of file %s is not implemented.", file_path)


def iterate_rdf_triples(file_path):
    """
    A function that iterates over the lines of an rdf file and parse the lines.
    :param file_path:
    :return: generator
    """
    open_fn = open_file(file_path)
    rdf_parser = get_rdf_parser(file_path)
    with open_fn(file_path, "r") as in_file:
        for rdf_line in in_file:
            # we use a dummy "." base uri to parse the triples
            # and satisfy their api.
            rdf_stream = rdf_parser.parse_string_as_stream(rdf_line, ".")
            for statement in rdf_stream:
                yield statement.subject, statement.predicate, statement.object


def tuple_generator(file_path, prefix=None):
    """
    A funtion that returns a tuple generator
    :param file_path: str: file_to_process
    :return: tuple
    """
    rdf_tuple_iterator = iterate_rdf_triples(file_path)
    counter = 0
    for subj, _, obj in rdf_tuple_iterator:
        
        subj = unicode(subj)
        obj = unicode(obj)
        if prefix:
            subj = subj.replace(prefix, "")
            obj = obj.replace(prefix, "")
        counter += 1
        if counter % 1000 == 0:
            logger.info("Processed %i items.", counter)

        yield subj, obj


def generate_subject_object_map(file_path, prefix=None):
    """
    A function that generates a map from subj->obj
    :param file_path: str: file_to_process
    :return: dict
    """
    
    subj_obj_generator = tuple_generator(file_path, prefix)
    return dict(subj_obj_generator)


def generate_title_id_map(redirects_file_path, title_ids_file_path, output_file_path=None):
    """
    A function that generates a map from subj->obj
    :param redirects_file_path: str: path_to_transitive_redirects
    :param title_ids_file_path: str: path_to_page_ids
    :param output_file_path: str: path to where resulting id map is saved

    """
    resolved_title_id_map = dict()
    redirects_map = generate_subject_object_map(redirects_file_path, DBPEDIA_RES_URI)
    title_ids_map = generate_subject_object_map(title_ids_file_path, DBPEDIA_RES_URI)
    counter = 0
    for title, page_id in title_ids_map.items():
        # Let's get the redirect and return the original title if no redirect
        title = redirects_map.get(title, title)
        # Check to see if title in the id map.
        if title in title_ids_map:
            page_id = title_ids_map[title]
        else:
            logger.warning("Could not find a page id for title %s, weird.", page_id)
        # Add title there
        if title not in resolved_title_id_map:
            resolved_title_id_map[title] = page_id
        else:
            logger.debug("Skipping %s because it's already there.", title)
        # increment counter
        counter += 1
        if counter % 1000 == 0:
            logger.info("Processed %i items.", counter)
    # Dump the resolved file
    if output_file_path:
        logger.info("Dumping processed id map to %s .", output_file_path)
        with codecs.open(output_file_path, "w") as out_file:
            pickle.dump(resolved_title_id_map, out_file, pickle.HIGHEST_PROTOCOL)
        logger.info("Finished.")
    return resolved_title_id_map
