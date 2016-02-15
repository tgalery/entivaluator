import codecs
try:
    import cPickle as pickle
except ImportError:
    import pickle
import re
import multiprocessing

import bz2file
import gzip
import RDF
from six.moves.urllib.parse import unquote
from six import binary_type

from utils.logger import get_logger

RDF_LINE = re.compile(r"^\s*<([^>]+)>\s+<([^>]+)>\s+(.+)\s*\.", re.UNICODE)
URL = re.compile(r"^<([^>]+)>")
LITERAL = re.compile(r"^\"(.*)\"?(?:\^\^.*)")
DBPEDIA_RES_URI = "http://dbpedia.org/resource/"
CHARMASK = """ '"\n"""

logger = get_logger()


def convert_to_unicode(input_str):
    """
    A function for converting a unicode to by string

    :param input_str: str or bytes: string to be converted
    :return: unicode
    """
    if isinstance(input_str, binary_type):
        input_str = input_str.decode("utf-8")
    return input_str


def parse_line(line):
    """
    A function that parses rdf on the basis of regexes.
    """
    subj = None
    pred = None
    obj = None

    line_match = RDF_LINE.match(line)
    if line_match is not None:
        subj = unquote(line_match.group(1).strip(CHARMASK))
        pred = unquote(line_match.group(2).strip(CHARMASK))
        url_match = URL.match(line_match.group(3))
        if url_match is not None:
            return subj, pred, url_match.group(1)
        literal_match = LITERAL.match(line_match.group(3))
        if literal_match is not None:
            return subj, pred, literal_match.group(1)
    return subj, pred, obj


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
    with open_fn(file_path, "r", encoding="utf-8") as in_file:
        for rdf_line in in_file:
            # we use a dummy "." base uri to parse the triples
            # and satisfy their api.
            rdf_stream = rdf_parser.parse_string_as_stream(rdf_line, ".")
            for statement in rdf_stream:
                yield statement.subject, statement.predicate, statement.object

def read_rdf(file_path):
    open_fn = open_file(file_path)
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    return pool.imap(parse_line, open_fn(file_path), chunksize=1000)


def tuple_generator(file_path, prefix=None):
    """
    A funtion that returns a tuple generator
    :param file_path: str: file_to_process
    :return: tuple
    """
    #rdf_tuple_iterator = iterate_rdf_triples(file_path)
    rdf_tuple_iterator = read_rdf(file_path)
    counter = 0
    for subj, _, obj in rdf_tuple_iterator:
        if subj and obj:
            subj = convert_to_unicode(subj)
            obj = convert_to_unicode(obj)
            if prefix:
                subj = subj.replace(prefix, "")
                obj = obj.replace(prefix, "").strip(CHARMASK)
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


