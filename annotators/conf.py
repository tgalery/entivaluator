from os.path import realpath, join

try:
    spotlight_path = join(realpath(__file__).rsplit("/annotators")[0],
                          "resources/wiki_title_to_id.pkl")
except Exception:
    spotlight_path = None


TITLE_TO_ID = {
    "spotlight": spotlight_path
}

ENDPOINTS = {
    "spotlight": "http://localhost:2222/rest/annotate"
}
