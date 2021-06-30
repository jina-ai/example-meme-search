from jina import Flow, Document, DocumentArray
# from jina.parsers.helloworld import set_hw_chatbot_parser
import click
from config import (
    port,
    workdir,
    datafile,
    max_docs,
    random_seed,
    model
)
from helper import deal_with_workspace
# fromrs import MyTransformer, MyIndexer
from jinahub.text.encoders.transform_encoder import TransformerTorchEncoder
from executors.disk_indexer import DiskIndexer

try:
    __import__("pretty_errors")
except ImportError:
    pass


def prep_json(input_file, num_docs=None, shuffle=True):
    import json

    docs = DocumentArray()
    memes = []
    print(f"Processing {input_file}")
    with open(input_file, "r") as file:
        raw_json = json.loads(file.read())

    for template in raw_json:
        for meme in template["generated_memes"]:
            meme["template"] = template["name"]
        memes.extend(template["generated_memes"])

    if shuffle:
        import random

        random.seed(random_seed)
        random.shuffle(memes)

    for meme in memes[:num_docs]:
        doctext = f"{meme['template']} - {meme['caption_text']}"
        doc = Document(text=doctext)
        doc.tags = meme
        docs.extend([doc])

    return docs


# def run_flow(inputs, args) -> None:
    # """
    # Execute the app store example. Indexes data and presents REST endpoint
    # :param inputs: Documents or DocumentArrays to input
    # :args: arguments like port, workdir, etc
    # :return: None
    # """

    # # Create Flow and add
    # #   - MyTransformer (an encoder Executor)
    # #   - MyIndexer (a simple indexer Executor)
    # flow = (
        # Flow()
        # .add(
            # uses=TransformerTorchEncoder,
            # pretrained_model_name_or_path=backend_model,
            # name="encoder",
            # max_length=50,
        # )
        # .add(uses=MyTransformer, parallel=args.parallel)
        # .add(uses=MyIndexer, workspace=args.workdir)
    # )

    # # Open the Flow
    # with flow:
        # # Start index pipeline, taking inputs then printing the processed DocumentArray
        # flow.post(on="/index", inputs=inputs, on_done=print)

        # # Start REST gateway so clients can query via Streamlit or other frontend (like Jina Box)
        # flow.use_rest_gateway(args.port_expose)

        # # Block the process to keep it open. Otherwise it will just close and no-one could connect
        # flow.block()


# if __name__ == "__main__":

    # # Get chatbot's default arguments
    # args = set_hw_chatbot_parser().parse_args()

    # # Change a few things
    # args.port_expose = backend_port
    # args.workdir = backend_workdir

    # docs = prep_json(backend_datafile, max_docs=max_docs)

    # # # Run the Flow
    # run_flow(inputs=docs, args=args)


def index(num_docs: int = max_docs):
    """
    Build an index for your search
    :param num_docs: maximum number of Documents to index
    """
    flow = (
        Flow()
        .add(
            uses=TransformerTorchEncoder,
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=DiskIndexer, workspace=workdir, name="indexer")
        # .add(uses=LMDBIndexer, workspace=workdir, name="indexer")
    )

    with flow:
        flow.post(
            on="/index",
            inputs=prep_json(input_file=datafile, num_docs=num_docs),
            request_size=64,
            read_mode="r",
        )


def query_restful():
    """
    Query your index
    """
    flow = (
        Flow()
        .add(
            uses="TransformerTorchEncoder",
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=DiskIndexer, workspace=workdir, name="indexer")
        # .add(uses=LMDBIndexer, workspace=workdir, name="indexer")
    )

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
        deal_with_workspace(dir_name=workdir, should_exist=False, force_remove=force)
        index(num_docs=num_docs)

    if task == "query_restful":
        deal_with_workspace(dir_name=workdir, should_exist=True)
        query_restful()


if __name__ == "__main__":
    main()
