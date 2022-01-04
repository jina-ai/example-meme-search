from jina import Client, Document
from config import TEXT_PORT, TEXT_SERVER, IMAGE_PORT, IMAGE_SERVER, TOP_K


class UI:
    about_block = """

    ### About

    This is a meme search engine using [Jina's neural search framework](https://github.com/jina-ai/jina/).

    - [Live demo](https://examples.jina.ai/memes)
    - [Play with it in a notebook](https://colab.research.google.com/github/jina-ai/workshops/blob/main/memes/meme_search.ipynb) (text-only)
    - [Repo](https://github.com/alexcg1/jina-meme-search)
    - [Dataset](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset)
    """

    css = f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
"""


headers = {"Content-Type": "application/json"}


def search_by_text(input, server=TEXT_SERVER, port=TEXT_PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        parameters={"limit": limit},
        return_results=True,
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches


def search_by_file(document, server=IMAGE_SERVER, port=IMAGE_PORT, limit=TOP_K):
    """
    Wrap file in Jina Document for searching, and do all necessary conversion to make similar to indexed Docs
    """
    client = Client(host=server, protocol="http", port=port)
    query_doc = document
    query_doc.convert_buffer_to_image_blob()
    query_doc.set_image_blob_shape((64, 64))
    query_doc.set_image_blob_normalization()
    response = client.search(
        query_doc,
        parameters={"limit": limit},
        return_results=True,
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches


def convert_file_to_document(query):
    data = query.read()

    doc = Document(buffer=data)
    print(doc)

    return doc


def get_image_url(file_path, domain="http://i.imgflip.com/"):
    filename = file_path.split("/")[-1]
    url = domain + filename

    return url
