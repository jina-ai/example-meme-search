import click
from jina import Flow
from config import WORKSPACE_DIR, NUM_DOCS, DATA_DIR, REQUEST_SIZE, PORT, BENCHMARK
from executors import ImageNormalizer
from helper import generate_docs, check_gpu
from datetime import datetime

encoder = "jinahub://CLIPImageEncoder/"

if check_gpu():
    print("Using GPU")
    encoder += "-gpu"
    uses_with = {"device": "cuda"}
else:
    print("Using CPU")
    uses_with = {"device": "cpu"}

flow = (
    Flow(protocol="http", port=PORT)
    .add(name="image_normalizer", uses=ImageNormalizer)
    .add(
        name="meme_image_encoder",
        uses=encoder,
        uses_metas={"workspace": WORKSPACE_DIR},
        uses_with=uses_with,
        gpus="all",
        volumes="./data:/encoder/data",
        install_requirements=True,
    )
    .add(
        name="meme_image_indexer",
        uses="jinahub://PQLiteIndexer/",
        uses_with={
            "limit": 12,
            "dim": 512, # SpaCy en_core_md uses 300 dims
            "include_metadata": True
        },
        # volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True,
    )
)


def index(num_docs=NUM_DOCS):
    docs = generate_docs(DATA_DIR, num_docs)

    with flow:
        if BENCHMARK:
            start_time = datetime.now()
        flow.index(inputs=docs, show_progress=True, request_size=REQUEST_SIZE)
        if BENCHMARK:
            end_time = datetime.now()
            difference = end_time - start_time
            print(difference.seconds)
            minutes = difference.seconds / 60
            print(f"Indexing took {minutes} minutes ({minutes/60} hours)")




def search():
    with flow:
        flow.block()


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
