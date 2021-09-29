import requests
import magic
import os

repo_banner_file = os.path.abspath("./eah.svg")

class UI:

    repo_banner = """
<div xmlns="http://www.w3.org/1999/xhtml" style="background-color: #fffbdd; text-align:center; margin-left: auto; margin-right: auto; border-radius: 6px; border-style: solid; border-width: 1px; border-color: #b0880033; color: #24292e; width: 100%">
            <style>
            p {
                font-family: sans-serif;
                font-size: max(1em, 12px);
            }
            </style>
            <p>
                <h3 style="color:#000">⭐ Like what you see?</h3>
                Star <a href="https://github.com/jina-ai/jina/" target="_blank">Jina's GitHub repo</a> and join our <a href="https://slack.jina.ai">Slack community</a>
            </p>
        </div>
    """

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


def search_by_text(query: str, endpoint: str, top_k: int) -> dict:
    """search_by_text.

    :param query:
    :type query: str
    :param endpoint:
    :type endpoint: str
    :param top_k:
    :type top_k: int
    :rtype: dict
    """
    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


def search_by_file(endpoint, top_k, filename="query.png"):
    """search_by_file.

    :param endpoint:
    :param top_k:
    :param filename:
    """
    filetype = magic.from_file(filename, mime=True)
    filename = os.path.abspath(filename)


    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": [{"uri": "'
        + filename
        + '", "mime_type": "'
        + filetype
        + '"}]}'
    )
    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    matches = content["data"]["docs"][0]["matches"]

    return matches


def create_temp_file(query, output_file="/tmp/query.png"):
    """create_temp_file.

    :param query:
    :param output_file:
    """
    data = query.read()

    with open(output_file, "wb") as file:
        file.write(data)

    return output_file
