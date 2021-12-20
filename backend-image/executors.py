from jina import Executor, requests, Document, DocumentArray


class ImageNormalizer(Executor):
    @requests
    def process_images(self, docs, **kwargs):
        if type(docs) == Document:
            docs = DocumentArray([docs])

        for doc in docs:
            doc.load_uri_to_image_blob()
            doc.set_image_blob_shape((64, 64))
            doc.set_image_blob_normalization()
