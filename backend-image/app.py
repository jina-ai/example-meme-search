import click
import sys
import os
from jina import Flow, Document
from config import WORKSPACE_DIR, NUM_DOCS, DATA_DIR, REQUEST_SIZE, PORT
from executors import ImageNormalizer
from helper import print_result, generate_docs, check_gpu

encoder = "jinahub://CLIPImageEncoder/v0.3"

if check_gpu():
    encoder += "-gpu"

flow = (
    Flow()
    .add(
        uses="jinahub://DocCache",
        install_requirements=True
    )
    .add(name="image_normalizer", uses=ImageNormalizer)
    .add(
        name="meme_image_encoder",
        uses="jinahub://CLIPImageEncoder/v0.3",
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes="./data:/encoder/data",
        install_requirements=True,
        # force=True
    )
    .add(
        name="meme_image_indexer",
        uses="jinahub://SimpleIndexer/v0.11",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True,
        # force=True
    )
)


def index(num_docs=NUM_DOCS):
    docs = generate_docs(DATA_DIR, num_docs)

    with flow:
        flow.index(inputs=docs, show_progress=True, request_size=REQUEST_SIZE)


def search():

    with flow:
        flow.protocol = "http"
        flow.port_expose = PORT
        flow.block()


def search_grpc():
    filename = sys.argv[2]
    query = Document(uri=filename)

    with flow:
        flow.search(
            query,
            on_done=print_result,
            parameters={"top_k": 5},
            show_progress=True,
        )

@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(num_docs=num_docs)
    elif task == "search":
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()

# print(f"DEBUG {sys.argv=}")
# if len(sys.argv) < 1:
    # print("Supported arguments: index, search, search_grpc")
# if sys.argv[1] == "index":
    # index()
# elif sys.argv[1] == "search":
    # search()
# elif sys.argv[1] == "search_grpc":
    # search_grpc()
# else:
    # print("Supported arguments: index, search, search_grpc")
