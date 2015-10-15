#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import requests
import sys
import time
from flask import Flask, request

from leothebot import telegram, leo


app = Flask(__name__)


@app.route("/levtolstoy/<code>", methods=['POST'])
def webhook_callback(code=None):
    if code != app.config['webhook_code']:
        return ""

    payload = json.loads(request.data)
    app.config['leo'].incoming_message(payload=payload)

    return "OK"


def main():
    if len(sys.argv) < 2 or not (sys.argv[1] and os.path.isfile(sys.argv[1])):
        print("Use: levtolstoy <config file path>")
        return 1

    config = json.load(open(sys.argv[1], "r"))
    app.config.update(config)

    # Initialize Leo
    app.config['telegram'] = telegram.TelegramAPI(config["telegram_token"])
    app.config['leo'] = leo.Leo(telegram=app.config['telegram'])
    app.config['leo'].restore_state()

    # Enable Telegram's webhook
    app.config['telegram'].initialize_webhook(
        endpoint="{0}/levtolstoy/{1}".format(
            config["root_url"], config["webhook_code"]),
        certificate=config["certificate"])

    # Enter Flask's loop
    app.run(port=config.get('port', None))

    # Save state and shutdown
    app.config['telegram'].disable_webhook()
    app.config['leo'].persist_state()

if __name__ == "__main__":
    r = main()
    sys.exit(r)
