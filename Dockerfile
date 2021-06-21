FROM pytorch/pytorch:latest

RUN apt-get update
RUN apt-get -y install wget

COPY . /workspace
WORKDIR /workspace

RUN sh ./get_data.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]

LABEL author="Alex C-G (alex.cg@jina.ai)"
LABEL type="app"
LABEL kind="example"
LABEL avatar="None"
LABEL description="Meme text search example using Jina"
LABEL documentation="https://github.com/alexcg1/jina-meme-search-example"
LABEL keywords="[NLP, memes, text, jina, example, search]"
LABEL license="apache-2.0"
LABEL name="jina-meme-text-search-example"
LABEL platform="linux/amd64"
LABEL update="None"
LABEL url="https://github.com/alexcg1/jina-meme-search-example"
LABEL vendor="Jina AI Limited"
LABEL version="0.2"
