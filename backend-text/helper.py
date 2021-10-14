import os
import shutil
import sys
import json
from jina import Document, DocumentArray
from config import random_seed


def prep_docs(input_file, num_docs=None, shuffle=True):
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
        doc.tags["uri_absolute"] = "http" + doc.tags["image_url"]
        docs.extend([doc])

    return docs


def deal_with_workspace(
    dir_name, should_exist: bool = False, force_remove: bool = False
):
    if should_exist:
        if not os.path.isdir(dir_name):  # It should exist but it doesn't exist
            print(
                f"The directory {dir_name} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)

    if not should_exist:  # it shouldn't exist
        if os.path.isdir(dir_name):
            if not force_remove:
                print(
                    f"\n +----------------------------------------------------------------------------------+ \
                        \n |                                   🤖🤖🤖                                         | \
                        \n | The directory {dir_name} already exists. Please remove it before indexing again.  | \
                        \n |                                   🤖🤖🤖                                         | \
                        \n +----------------------------------------------------------------------------------+"
                )
                sys.exit(1)
            else:
                shutil.rmtree(dir_name)
