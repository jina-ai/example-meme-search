import os

MODEL = "en_core_web_md" # Which SpaCy model do we use?
PORT = 45679
WORKSPACE_DIR = "workspace"
CACHE_DIR = os.path.expanduser('~/.cache')
DATAFILE = "../data/memes.json"
MAX_DOCS = 1000
RANDOM_SEED = 1337
