from jina import Executor, requests, Document, DocumentArray
import os


class UriToBlob(Executor):
    @requests
    def uri_to_blob(self, docs, **kwargs):
        for doc in docs:
            doc.tags["uri"] = doc.uri
            doc.tags["uri_absolute"] = os.path.abspath(doc.uri)
            doc.convert_image_uri_to_blob()

class ImageNormalizer(Executor):
    @requests
    def process_images(self, docs, **kwargs):
        if type(docs) == Document:
            docs = DocumentArray([docs])

        for doc in docs:
            doc.load_uri_to_image_blob()
            doc.set_image_blob_shape((64, 64))
            doc.set_image_blob_normalization()
