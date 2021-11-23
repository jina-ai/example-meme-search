import click
from jina import Flow
from config import port, WORKSPACE_DIR, datafile, max_docs, model
from helper import deal_with_workspace, prep_docs


flow = (
    Flow()
    # .add(
        # name="remove_duplicates",
        # uses="jinahub+docker://DocCache",
        # uses_with={"fields": ["text"]},
    # )
    # .add(
        # name="remove_dead_urls",
        # uses="jinahub+docker://RemoveDeadURLs",
        # # uses="jinahub://RemoveDeadURLs",
        # uses_with={"tag": "uri_absolute"},
        # # install_requirements=True
    # )
    .add(
        name="meme_text_encoder",
        uses="jinahub+docker://SpacyTextEncoder/v0.1",
        uses_with={"model_name": model},
    )
    .add(
        name="meme_text_indexer",
        uses="jinahub+docker://SimpleIndexer/v0.7",
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
    )
)


def index(num_docs: int = max_docs):
    """
    Build an index for your search
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
    Query your index
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

    if task == "query_restful":
        deal_with_workspace(dir_name=WORKSPACE_DIR, should_exist=True)
        query_restful()


if __name__ == "__main__":
    main()
