#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import requests
import string
import sys
import time
import yaml

from klein import Klein
from twisted.internet.defer import inlineCallbacks, returnValue

from leothebot import telegram, leo
from leothebot.state import state


app = Klein()


@app.route("/levtolstoy/<code>", methods=['POST'])
@inlineCallbacks
def webhook_callback(request, code=None):
    if code != state.config['webhook_code']:
        returnValue('')

    payload = json.loads(request.data)
    yield state.actors['leo'].incoming_message(payload=payload)

    returnValue('')


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
    state.config.update(config)

    # Initialize Leo
    state.actors['telegram'] = telegram.TelegramAPI(
        token=config['server']['telegram_token'])
    state.actors['leo'] = leo.Leo(telegram=state.actors['telegram'])
    state.actors['leo'].restore_state()
    state.config['webhook_code'] = generate_webhook_code()

    # Enable Telegram's webhook
    state.actors['telegram'].initialize_webhook(
        endpoint="{0}/levtolstoy/{1}".format(
            state.config['server']['root_url'],
            state.config['webhook_code']),
        certificate=state.config['server']['certificate'])

    # Enter Klein's loop
    app.run(
        host=state.config['server']['host'],
        port=state.config['server']['port'])

    # Save state and shutdown
    state.actors['telegram'].disable_webhook()
    state.actors['leo'].persist_state()

if __name__ == '__main__':
    r = main()
    sys.exit(r)
