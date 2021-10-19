import sys
import os
from jina import Flow, DocumentArray
from jina.types.document.generators import from_files
from executors import UriToBlob

NUM_DOCS = 10
IMAGE_SIZE = 48 # Resize to 48 x 48 for faster processing
REQUEST_SIZE = 16 # Lower = lower memory usage
FORMATS = ["jpg", "png", "jpeg"]
DATA_DIR = "data"
WORKSPACE_DIR = "workspace"

flow = (
    Flow()
    # .add(uses=UriToBlob, name="processor") # Embed image in doc, not just filename
    .add(
        name="image_normalizer",
        uses="jinahub+docker://ImageNormalizer",
        uses_with={"target_size": IMAGE_SIZE},
        volumes="./data:/workspace/data",
        force=True
    )
    .add(
        name="meme_image_encoder",
        uses="jinahub+docker://CLIPImageEncoder",
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes="./data:/encoder/data",
        force=True
    )
    .add(
        name="meme_image_indexer",
        uses="jinahub+docker://SimpleIndexer/old",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
    )
)

def generate_docs(directory, num_docs=NUM_DOCS, formats=FORMATS):
    docs = DocumentArray()
    for format in formats:
        docarray = DocumentArray(from_files(f"{directory}/**/*.{format}", size=num_docs))
        docs.extend(docarray)

    return docs[:num_docs]
        

def index():
    if os.path.exists(WORKSPACE_DIR):
        print(f"'{WORKSPACE_DIR}' folder exists. Please delete")
        sys.exit()

    docs = generate_docs(DATA_DIR, NUM_DOCS)

    with flow:
        flow.index(inputs=docs, show_progress=True, request_size=REQUEST_SIZE)


def query_restful():
    flow.protocol = "http"
    flow.port_expose = 12345

    with flow:
        flow.block()


if len(sys.argv) < 1:
    print("Supported arguments: index, query_restful, query_grpc")
if sys.argv[1] == "index":
    index()
elif sys.argv[1] == "query_restful":
    query_restful()
else:
    print("Supported arguments: index, query_restful")
