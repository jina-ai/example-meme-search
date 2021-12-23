import click
from jina import Flow
from config import port, WORKSPACE_DIR, datafile, max_docs, model
from helper import deal_with_workspace, prep_docs


flow = (
    Flow()
    .add(
        name="meme_text_encoder",
        uses=f"jinahub://SpacyTextEncoder/v0.3",
        uses_with={"model_name": model},
        install_requirements=True
    )
    .add(
        name="meme_text_indexer",
        uses=f"jinahub://SimpleIndexer/v0.11",
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True
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


def search():
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
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    if task == "index":
        deal_with_workspace(
            dir_name=WORKSPACE_DIR, should_exist=False, force_remove=force
        )
        index(num_docs=num_docs)
    elif task == "search":
        deal_with_workspace(dir_name=WORKSPACE_DIR, should_exist=True)
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
