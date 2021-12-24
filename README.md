# Jina meme search

In this repo you can find three folders to help build your own meme search engine powered by [Jina](https://github.com/jina-ai/jina/).

- [backend-text](./backend-text) - Uses SpaCy to encode and search through meme captions
- [backend-image](./backend-image) - Uses CLIP to encode and search through meme images
- [frontend](./frontend) - A [Streamlit](https://streamlit.io) frontend for the whole thing 

Each of these can be run independently. You can play with a [live demo](https://examples.jina.ai/memes) or [notebook](https://github.com/jina-ai/workshops/tree/main/memes) (text-search only) to get a feel for it.

## Note

I'm still revamping the README's, so documentation might not be fully up-to-date for a little while.


## Instructions

### Set up

- Create a virtual environment
- `python get_memes.py 200000`  (where 200000 is the number of memes you want to download)

## Text search

```shell
cd backend-text
pip install -r requirements.txt
python app.py -t index -n 1000   # Index 1000 memes
python app.py -t search          # Open RESTful gateway
```

## Image search

Edit `app.py` to set number of memes to index.

```shell
cd backend-image
pip install -r requirements.txt
python app.py -t index -n 1000   # Index 1000 memes
python app.py -t search          # Open RESTful gateway
```

## Frontend

```shell
cd frontend
pip install -r requirements.txt
streamlit app.py
```

## Via `docker-compose`

Note: This opens up the search interfaces for meme search, including the frontend. It **doesn't** index the data. Be sure to do that beforehand.

1. Follow instructions above for setup and indexing (don't query anything yet)
2. In root dir, `docker-compose up`

## Troubleshooting

### Running out of memory

If you're on Linux you can create a swapfile:

```shell
dd if=/dev/zero of=swapfile bs=1M count=10240 status=progress   # 10240mb = 10gb
chmod 600 swapfile
mkswap swapfile
swapon swapfile
```
