from jina import DocumentArray
import json
from jina.types.document.generators import from_ndjson

input_file = "../../data/memes.json"

def json_doc_generator(input_file, primary_field=None):
    with open(input_file, 'r') as file:
        content = json.loads(file.read())
        print(content[0])
        # for row in content:
            # print(type(row))

json_doc_generator(input_file)
# with open('data/db.json') as jsonfile:
    # data = json.loads(jsonfile.read())
    # memes = data["_default"]
    # memes_json = json.dumps(memes)
    # # docs = DocumentArray(from_ndjson(memes))

# with open('data/memes.json', 'w') as file:
    # file.write(memes_json)

