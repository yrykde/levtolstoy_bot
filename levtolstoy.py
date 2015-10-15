#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import requests
import sys
import time
from flask import Flask, request, g
app = Flask(__name__)


QUOTE_API_ENDPOINT = "http://api.forismatic.com/api/1.0/"
TG_API_ENDPOINT = "https://api.telegram.org/bot"

CONFIG = {}


class TelegramAPIError(Exception):
    pass


class TelegramAPI(object):
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def send(self, command, params={}):
        url = "{0}{1}/{2}".format(
            self.endpoint,
            self.token,
            command)
        response = requests.post(url=url, data=params)
        print("url=%s" % url)

        if not response.ok:
            raise TelegramAPIError

        return response.json()

    def initialize_webhook(self, url, certificate):
        r = self.send(
            command="setWebhook",
            params={"url": url,
                    "certificate": certificate})
        print("webhook_url=%s" % url)
        print(r)

    def disable_webhook(self):
        r = self.send(
            command="setWebhook",
            params={"url": ""})

        print(r)


def get_random_quote(lang='ru'):
    random.seed(time.time())

    quote_params = {
        'method': 'getQuote',
        'key': '{0}'.format(random.randint(100, 999999)),
        'format': 'json',
        'lang': lang}

    response = requests.post(
        url="http://api.forismatic.com/api/1.0/",
        data=quote_params)

    quote = "пукнул, сорян"

    if not response.ok:
        return quote

    try:
        quote = response.json()['quoteText']
    except KeyError:
        pass

    return quote


@app.route("/levtolstoy/<code>", methods=['POST'])
def webhook_callback(code=None):
    if code != app.config["webhook_code"]:
        return ""

    print("request.data = %r" % request.data)
    print("request.form = %r" % request.form)
    return "OK"


def main():
    if len(sys.argv) < 2 or not (sys.argv[1] and os.path.isfile(sys.argv[1])):
        print("Use: levtolstoy <config file path>")
        return 1

    global CONFIG
    CONFIG = json.load(open(sys.argv[1], "r"))
    app.config.update(CONFIG)

    app.config['telegram'] = telegram = \
        TelegramAPI(TG_API_ENDPOINT, CONFIG["telegram_token"])

    telegram.initialize_webhook(
        url="{0}/levtolstoy/{1}".format(
            CONFIG["root_url"], CONFIG["webhook_code"]),
        certificate=CONFIG["certificate"])

    app.run(port=CONFIG.get('port', None))

    telegram.disable_webhook()

if __name__ == "__main__":
    r = main()
    sys.exit(r)
