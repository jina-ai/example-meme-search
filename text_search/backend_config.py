# in executors.py
# backend_model = "sentence-transformers/msmarco-distilbert-base-v3"
backend_model = "sentence-transformers/paraphrase-distilroberta-base-v1"
# backend_model = "distilbert-base-uncased"
backend_top_k = 10

# in app.py
backend_port = 45679
backend_workdir = "workspace"
backend_datafile = "../../data/memes.json"
max_docs = 5000
