from jina import Executor, requests
from docarray import Document, DocumentArray


class ImageNormalizer(Executor):
    @requests(on="/index")
    def process_images(self, docs, **kwargs):
        if type(docs) == Document:
            docs = DocumentArray([docs])

        for doc in docs:
            doc.load_uri_to_image_tensor()
            doc.set_image_tensor_shape((64, 64))
            doc.set_image_tensor_normalization()
