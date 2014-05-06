pymd-weekpaper
==============

weekly working record base on markdown

## Requirements

```
pip install tornado
pip install dateutil
```

## Quick Start

1. run `python serve.py`, a new markdown file will be created in `posts/` named like `20140505 Week.md`
2. edit `20140505 Week.md`
3. browser in `http://127.0.0.1:5566/`

## Features

1. `/` browser lastest week's post
2. `/-1` browser last week's post
3. `/md` preview markdown in html
4. `/last` browser last week's post

## Sync posts

sync dir `posts/`

1. [坚果云](http://jianguoyun.com)
2. [Dropbox](https://dropbox.com)

## TODO

1. refactor code
2. change web server to flask
3. add README for `sync posts`
