model = "en_core_web_md" # Which SpaCy model do we use?
port = 45679
WORKSPACE_DIR = "workspace"
datafile = "./data/memes.json"
max_docs = 1000
random_seed = 1337

# If things go wrong because of code rot, try changing these
spacy_executor_ver = "latest"
simpleindexer_ver = "latest"
