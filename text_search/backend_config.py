# in executors.py
# backend_model = "sentence-transformers/msmarco-distilbert-base-v3"
backend_model = "sentence-transformers/paraphrase-distilroberta-base-v1"
# backend_model = "distilbert-base-uncased"
backend_top_k = 10

# in app.py
backend_port = 45678
backend_workdir = "workspace"
backend_datafile = "../../data/memes.json"
primary_field = "caption_text" # Primary field in data file (this will be assigned to Document.text and indexed. Other fields are metadata only)
