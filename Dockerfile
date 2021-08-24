FROM jinaai/jina:2.0-py38

ARG docs_to_index=100

COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get -y install wget git && pip install -r requirements.txt && sh get_data.sh && python app.py -t index -n $docs_to_index

ENTRYPOINT ["python", "app.py" , "-t", "query_restful"]
