## Download data

Run either:

- `python get_memes.py 1000` to download 1,000 memes
- `sh get_pokemon.sh` to download Pokemon sprite images

## Index data

```sh
python app.py index
```

## Query data

```sh
python app.py query_restful
```

And then...

### via `curl`

Open a new terminal and use the command:

```sh
curl --request POST -d '{"parameters": {"top_k": 3}, "mode": "search",  "data": [{"uri":"data/1.png", "mime_type": "image/png"}]}' -H 'Content-Type: application/json' 'http://localhost:12345/search'
```

Where:

- `uri` is the URI to the image you want to query with
- `mime_type` is either `image/png` or `image/jpg` (depending on your query image)

### via frontend

Open a new terminal, and go to the `frontend` directory, then type:

1. Create a virtual environment, install dependencies
2. Run `streamlit run app.py`
