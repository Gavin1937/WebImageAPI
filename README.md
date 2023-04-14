
# Web Image API: A Python3 package to fetch info and download images from popular websites.

[![Pack Release Package](https://github.com/Gavin1937/WebImageAPI/actions/workflows/pack-release-package.yml/badge.svg)](https://github.com/Gavin1937/WebImageAPI/actions/workflows/pack-release-package.yml)

This python package is designed to fetch basic information and download images from popular image hosting websites & social medias.

This project is a complete rewrite of my [old project WebPicAPI](https://github.com/Gavin1937/WebPicAPI)


# Supported Websites:

* [pixiv](https://www.pixiv.net/)
* [twitter](https://twitter.com/)
* [danbooru](https://danbooru.donmai.us/)
* [yande.re](https://yande.re/)
* [konachan](https://konachan.com/)
* [weibo](https://m.weibo.cn/)
* [e-hentai](https://e-hentai.org/)


# Python Version: >= 3.8


# Dependencies

| Name                                                             | Version   |
|------------------------------------------------------------------|-----------|
| [pixivpy3](https://pypi.org/project/PixivPy/)                    | >= 3.7.2  |
| [tweepy](https://pypi.org/project/tweepy/)                       | >= 4.13.0 |
| [requests](https://pypi.org/project/requests/)                   | >= 2.28.2 |
| [requests-oauthlib](https://pypi.org/project/requests-oauthlib/) | >= 1.3.1  |
| [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)       | >= 4.12.0 |
| [lxml](https://pypi.org/project/lxml/)                           | >= 4.9.2  |


# Install

install after cloning source code

```sh
pip install .
```

or, install from github

```sh
pip install -U git+https://github.com/Gavin1937/WebImageAPI.git
```

or, download .whl file from [the latest release](https://github.com/Gavin1937/WebImageAPI/releases/latest)

and install it

```sh
pip install -U WebImageAPI-*-py3-none-any.whl
```

# Authentication

| Name    | Tutorials                                                                                                         |
|---------|-------------------------------------------------------------------------------------------------------------------|
| Pixiv   | [get pixiv refresh_token follow upbit's tutorial](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde) |
| Twitter | [get twitter consumer_key, consumer_secret, access_token, access_token_secret](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)  |


# [Documentaion](./doc/index.md)

# [Quick Start](./demo/quick_start.py)

