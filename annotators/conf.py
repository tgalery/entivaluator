from os.path import realpath, join

RESOURCES = {
    "title_to_id": join(realpath(__file__).rsplit("/annotators")[0],
                        "resources/wiki_title_to_id.pkl")
}

ENDPOINTS = {
    "spotlight": "http://localhost:2222/rest/annotate"
}
