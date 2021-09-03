# AI-powered meme search

This is a simple example to show how to build an AI-powered search engine for searching memes using the [Jina](https://github.com/jina-ai/jina/) framework. It indexes and searches a subset of the [imgflip dataset](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset) from Kaggle.

## Play with a live demo

On [Jina's examples site](http://examples.jina.ai)

## Instructions

### Clone this repo

```shell
git clone git@github.com:alexcg1/jina-meme-search-example.git
cd jina-meme-search-example
```

### Create a virtual environment

We wouldn't want our project clashing with our system libraries, now would we?

```shell
virtualenv env --python=python3.8 # Python versions >= 3.7 work fine
source env/bin/activate
```

### Get the data

```shell
sh get_data.sh
```

### Install everything

Make sure you're in your virtual environment first!

```shell
pip install -r requirements.txt
```

### Increase your swap space

We're dealing with big language models and quite long text passages. Macs can apparently dynamically allocate swap space, but on Manjaro Linux I manually created and activated a swapfile. Otherwise my computer with 16gb of RAM will just freeze up while indexing.

```shell
# Don't bother if you're on a Mac or have loads of memory
dd if=/dev/zero of=swapfile bs=1M count=10240 status=progress
chmod 600 swapfile
mkswap swapfile
swapon swapfile
```

You'll need to do this after every reboot. Or you can [read the instructions](https://wiki.archlinux.org/title/Swap#Manually) to mount it at startup.

### Run the program

`app.py` indexes the dataset then opens up a REST gateway for you to search:

```shell
cd jina-meme-search-example
python app.py -t index -n 100 # index 100 memes
python app.py -t query_restful # open the query flow to start searching
```

### Start the front end

See our [front end repo](https://github.com/alexcg1/jina-meme-search-frontend)

### Search from the terminal

```shell
curl --request POST -d '{"top_k":10,"mode":"search","data":["squidward school"]}' -H 'Content-Type: application/json' 'http://0.0.0.0:45678/search'
```

Where `hello world` is your query.

The results should be a big chunk of JSON containing the matching memes with captions and links to images. Or at least something close to matching. By default we're only indexing 1,000 memes. Also memes don't age well, so don't expect to find anything too new here!

## FAQ

### Why this dataset?

It contains a lot of metadata, including (working) links to images. I want to build a nice front-end to show off the search experience so graphical assets are vital. 

### How can I change basic settings?

Edit `text_search/backend_config.py`
