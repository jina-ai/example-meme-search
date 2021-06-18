# AI-powered app store search

![](./video.gif)

This is a simple example to show how to build an AI-powered search engine for an app store using the [Jina](https://github.com/jina-ai/jina/) framework. It indexes and searches a subset of the [17K Mobile Strategy Games dataset](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games) from Kaggle.

## Instructions

### Clone this repo

```shell
git clone git@github.com:alexcg1/jina-app-store-example.git
cd jina-app-store-example
```

### Create a virtual environment

We wouldn't want our project clashing with our system libraries, now would we?

```shell
virtualenv env --python=python3.8 # Python versions >= 3.7 work fine
source env/bin/activate
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
cd backend
python app.py
```

### Start the front end

In another terminal:

```sh
cd jina-app-store-example/
source env/bin/activate
cd frontend
streamlit app.py
```

Then open http://localhost:8501 in your browser

### Search from the terminal

```shell
curl --request POST -d '{"top_k":10,"mode":"search","data":["hello world"]}' -H 'Content-Type: application/json' 'http://0.0.0.0:45678/search'
```

Where `hello world` is your query.

The results should be a big chunk of JSON containing the matching apps. Or at least something close to matching. By default we're only indexing 1,000 apps from a list that's a few years old (since this is just an example) so don't be surprised if your search for a specific title doesn't come up.

## FAQ

### Why this dataset?

It contains a lot of metadata, including (working) links to icons. I want to build a nice front-end to show off the search experience so graphical assets are vital. Plus stuff like ratings, descriptions, the works.

### The download/purchase buttons don't do anything

This is just a demo search engine. It has no functionality beyond that. 

### How can I change basic settings?

Edit `backend/appstore_config.py`
