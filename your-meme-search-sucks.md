# Your Stupid Meme Search Sucks and So Do You!

## So, why I can't I see <this meme>?

A couple of answers to that question!

1. The [dataset we're using](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset) only contains so many "meme types"
2. For the text search we indexed 200,000 memes - that's the whole dataset
3. For the image search we just indexed a subset of 1,000 since it's a lot more computationally expensive

## So just index more memes, duh!

We didn't expect this to explode so soon. We're doing this as we speak.

## Ugh, just use a better dataset

We use this dataset because it has rich metadata. That lets use use both text search and image search (because the text search searches the JSON metadata that includes the captions)

## My meme search is much better!

Awesome! We threw this together quickly and didn't expect it to blow up. And in just a few lines of code to boot.
