from jina import Flow, Document, DocumentArray
from jina.parsers.helloworld import set_hw_chatbot_parser
from config import (
    backend_port,
    backend_workdir,
    backend_datafile,
    max_docs,
    random_seed
)
from executors import MyTransformer, MyIndexer

try:
    __import__("pretty_errors")
except ImportError:
    pass


def prep_json(input_file, max_docs=None, shuffle=True):
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

    for meme in memes[:max_docs]:
        doctext = f"{meme['template']} - {meme['caption_text']}"
        doc = Document(text=doctext)
        doc.tags = meme
        docs.extend([doc])

    return docs


def run_flow(inputs, args) -> None:
    """
    Execute the app store example. Indexes data and presents REST endpoint
    :param inputs: Documents or DocumentArrays to input
    :args: arguments like port, workdir, etc
    :return: None
    """

    # Create Flow and add
    #   - MyTransformer (an encoder Executor)
    #   - MyIndexer (a simple indexer Executor)
    flow = (
        Flow()
        .add(uses=MyTransformer, parallel=args.parallel)
        .add(uses=MyIndexer, workspace=args.workdir)
    )

    # Open the Flow
    with flow:
        # Start index pipeline, taking inputs then printing the processed DocumentArray
        flow.post(on="/index", inputs=inputs, on_done=print)

        # Start REST gateway so clients can query via Streamlit or other frontend (like Jina Box)
        flow.use_rest_gateway(args.port_expose)

        # Block the process to keep it open. Otherwise it will just close and no-one could connect
        flow.block()


if __name__ == "__main__":

    # Get chatbot's default arguments
    args = set_hw_chatbot_parser().parse_args()

    # Change a few things
    args.port_expose = backend_port
    args.workdir = backend_workdir

    docs = prep_json(backend_datafile, max_docs=max_docs)

    # # Run the Flow
    run_flow(inputs=docs, args=args)
