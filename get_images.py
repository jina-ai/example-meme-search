import os
import requests
import sys
import json
import random
try:
    __import__("pretty_errors")
except ImportError:
    pass

input_file = './data/memes.json'
images_dir = './data/images'
max_docs = int(sys.argv[1])

if not os.path.isfile(input_file):
    print("Please run get_data.sh first")
    sys.exit()

if not os.path.isdir(images_dir):
    os.makedirs(images_dir)


with open(input_file, "r") as file:
    raw_json = json.loads(file.read())

os.chdir(images_dir)
memes = []
for template in raw_json:
    for meme in template["generated_memes"]:
        meme["template"] = template["name"]
    memes.extend(template["generated_memes"])

random.shuffle(memes)

for meme in memes[:max_docs]:
    filename = meme["image_url"].split('/')[-1]
    image_url = 'http:' + meme["image_url"]
    print(f"Downloading {image_url}")
    r = requests.get(image_url, allow_redirects=True)
    with open(filename, 'wb') as file:
        file.write(r.content)


