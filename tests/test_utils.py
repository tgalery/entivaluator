# -*- coding: utf-8 -*-
"""
Tests for the utils module
"""
from os.path import realpath
import unittest

from utils import io

BASE_DIR = realpath(__file__).rsplit("tests/", 1)[0]
PAGE_IDS = BASE_DIR + "test_files/page_ids.ttl"
REDIRECTS = BASE_DIR + "test_files/transitive_redirects.ttl"


class TestUtils(unittest.TestCase):
    """
    A class that tests the wikidata module
    """

    def test_generate_subject_object_map_page_ids(self):
        page_id_map = io.generate_subject_object_map(PAGE_IDS,
                                                     io.DBPEDIA_RES_URI)
        self.assertEqual(page_id_map["AccessibleComputing"], "10")

    def test_generate_subject_object_map_redirects(self):
        page_id_map = io.generate_subject_object_map(REDIRECTS,
                                                     io.DBPEDIA_RES_URI)
        self.assertEqual(page_id_map["AccessibleComputing"], "Computer_accessibility")

    def test_generate_title_id_map(self):
        resolved_title_id_map = io.generate_title_id_map(REDIRECTS, PAGE_IDS)
        self.assertEqual(resolved_title_id_map["Computer_accessibility"], "411964")
        # To review the test case below
        self.assertTrue("AccessibleComputing" not in resolved_title_id_map)
