# Fake sublime telegram bot sources
This is _FAKE_ sources just **_imitating_** the functionality similar 
to one by SublimeBot in Telegram

> For any legal or copyright issues please [contact me via email](mailto:super.mvk@yandex.ru)

## Prerequisites

* (Optionally) Install Python 3.8 and/or Docker
* Create `.env` file and put `TELEGRAM_BOT_API_TOKEN=<token>` there

## Installation

* Clone repository `git clone git@github.com:unaimillan/sublime-telegram-bot`
* Create virtual environment `python -m venv venv`
* Activate venv `source venv/bin/activate`
* Install all dependencies `pip3 install -r requirements.txt`

## Usage

Bot reads Telegram Bot Token from both `.env` file in current folder and also
`TELEGDAM_BOT_API_TOKEN` environmental variable

* Activate venv `source venv/bin/activate`
* Setup telegram bot token `export TELEGDAM_BOT_API_TOKEN=<token>`
* Start the bot `python3 main.py`

## Docker

* Build the image `docker build . -t <imagename>`
* Run docker image directly `docker run --rm --env-file=.env -it <imagename>` 
* or by `docker-compose` and `.env` file with token
