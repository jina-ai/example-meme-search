from jina import Document, DocumentArray
from config import NUM_DOCS, FORMATS


def generate_docs(directory, num_docs=NUM_DOCS, formats=FORMATS):
    docs = DocumentArray()
    for format in formats:
        docarray = DocumentArray.from_files(f"{directory}/**/*.{format}", size=num_docs)
        docs.extend(docarray)

    # docs = process_images(docs)

    return docs[:num_docs]


def process_images(images):
    if type(images) == Document:
        images = DocumentArray([images])

    for image in images:
        image.load_uri_to_image_blob()
        image.set_image_blob_shape((64, 64))
        image.set_image_blob_normalization()

    return images


def print_result(resp):
    """
    Callback function to receive results.

    :param resp: returned response with data
    """
    matches = []
    for doc in resp.docs:
        for match in doc.matches:
            kmi = match.uri
            matches.append(kmi)

        for match in doc.matches:
            print(f"{match.uri}")


def check_gpu():
    import GPUtil

    gpu_list = GPUtil.getAvailable()
    if len(gpu_list) > 0:
        return True
    else:
        return False
