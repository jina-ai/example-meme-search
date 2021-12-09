import click
from jina import Flow
from config import port, WORKSPACE_DIR, datafile, max_docs, model, spacy_executor_ver, simpleindexer_ver
from helper import deal_with_workspace, prep_docs


flow = (
    Flow()
    .add(
        name="meme_text_encoder",
        uses=f"jinahub+docker://SpacyTextEncoder/{spacy_executor_ver}",
        uses_with={"model_name": model},
    )
    .add(
        name="meme_text_indexer",
        uses=f"jinahub+docker://SimpleIndexer/{simpleindexer_ver}",
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
    )
)


def index(num_docs: int = max_docs):
    """
    Build index for your search
    :param num_docs: maximum number of Documents to index
    """
    with flow:
        flow.index(
            inputs=prep_docs(input_file=datafile, num_docs=num_docs),
            request_size=64,
            read_mode="r",
            show_progress=True,
        )


def query_restful():
    """
    Query index
    """
    with flow:
        flow.protocol = "http"
        flow.port_expose = port
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    if task == "index":
        deal_with_workspace(
            dir_name=WORKSPACE_DIR, should_exist=False, force_remove=force
        )
        index(num_docs=num_docs)
    elif task == "query_restful":
        deal_with_workspace(dir_name=WORKSPACE_DIR, should_exist=True)
        query_restful()
    else:
        print("Please add '-t index' or '-t query_restful' to your command")


if __name__ == "__main__":
    main()
