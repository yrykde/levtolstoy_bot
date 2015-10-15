#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import requests
import string
import sys
import time
import yaml

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


def generate_webhook_code(length=50):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length))


def main():
    if len(sys.argv) < 2 or not (sys.argv[1] and os.path.isfile(sys.argv[1])):
        print('Use: levtolstoy <config file path>')
        return 1

    with open(sys.argv[1], 'r') as config_f:
        config = yaml.load(config_f)
    app.config.update(config)

    # Initialize Leo
    app.config['telegram'] = telegram.TelegramAPI(
        token=config['server']['telegram_token'])
    app.config['leo'] = leo.Leo(telegram=app.config['telegram'])
    app.config['leo'].restore_state()
    app.config['webhook_code'] = generate_webhook_code()

    # Enable Telegram's webhook
    app.config['telegram'].initialize_webhook(
        endpoint="{0}/levtolstoy/{1}".format(
            app.config['server']['root_url'],
            app.config['webhook_code']),
        certificate=app.config['server']['certificate'])

    # Enter Flask's loop
    app.run(port=app.config['server']['port'])

    # Save state and shutdown
    app.config['telegram'].disable_webhook()
    app.config['leo'].persist_state()

if __name__ == '__main__':
    r = main()
    sys.exit(r)
