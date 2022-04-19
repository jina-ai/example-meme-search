import click
from jina import Flow
from config import PORT, DATAFILE, MAX_DOCS, MODEL, CACHE_DIR
from helper import prep_docs

flow = (
    Flow(protocol="http", port=PORT)
    .add(
        name="meme_text_encoder",
        uses="jinahub://SpacyTextEncoder/v0.4",
        uses_with={"model_name": MODEL},
        volumes=f"{CACHE_DIR}:/root/.cache",
        install_requirements=True,
    )
    .add(
        name="meme_text_indexer",
        uses="jinahub://PQLiteIndexer/0.2.6",
        uses_with={
            "limit": 12,
            "dim": 300, # SpaCy en_core_md uses 300 dims
            "include_metadata": True
        },
        install_requirements=True,
    )
)


def index(num_docs: int = MAX_DOCS):
    """
    Build index for your search
    :param num_docs: maximum number of Documents to index
    """
    with flow:
        flow.index(
            inputs=prep_docs(input_file=DATAFILE, num_docs=num_docs),
            request_size=64,
            read_mode="r",
            show_progress=True,
        )


def search():
    """
    Query index
    """
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task: str, num_docs: int):
    if task == "index":
        index(num_docs=num_docs)
    elif task == "search":
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
