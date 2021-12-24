import os
import sys
import json
import requests

MAX_DOCS = int(sys.argv[1])
JSON_URL = "https://jina-examples-datasets.s3.amazonaws.com/memes/memes.json"
OUTPUT_DIR = "./data"


def get_json(url, output_dir):
    if not os.path.isfile(f"{output_dir}/memes.json"):

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        print(f"Downloading {url} to '{output_dir}' directory")
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            with open(f"{output_dir}/memes.json", "wb") as file:
                file.write(r.content)


def prep_docs(input_file, max_docs, output_dir, random_seed=42, shuffle=True):
    print(f"Preparing {max_docs} Documents")

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

    os.chdir(output_dir)
    counter = 1
    for meme in memes[:max_docs]:

        # Download image

        url = f'http:{meme["image_url"]}'
        filename = meme["image_url"].split("/")[-1]
        print(f"Downloading {filename} - {counter}/{max_docs}")
        try:
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(r.content)
            counter += 1
        except:
            print(f"Error on {filename}, skipping.")


get_json(url=JSON_URL, output_dir=OUTPUT_DIR)
prep_docs("data/memes.json", max_docs=MAX_DOCS, output_dir=OUTPUT_DIR, shuffle=True)
