#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import string
import sys

from klein import Klein
from twisted.internet import defer, reactor

from leothebot import telegram, translate, leo
from leothebot.state import state


app = Klein()


@app.route("/levtolstoy/<code>", methods=['POST'])
def webhook_callback(request, code=None):
    if code != state.config['webhook_code']:
        return ''

    payload = json.loads(''.join([l for l in request.content]))
    state.actors['leo'].incoming_message(payload=payload)

    return 'ok'


def generate_webhook_code(length=50):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length))


def main():
    if len(sys.argv) < 2 or not (sys.argv[1] and os.path.isfile(sys.argv[1])):
        print('Use: levtolstoy <config file path>')
        return 1

    state.load_config(config_file=sys.argv[1])

    # Initialize Leo
    state.actors['telegram'] = telegram.TelegramAPI(
        token=state.config['server']['telegram_token'])
    state.actors['translate'] = translate.TranslateAPI(
        token=state.config['server']['google_translate_api_token'])
    state.actors['leo'] = leo.Leo(
        telegram=state.actors['telegram'],
        translate=state.actors['translate'])
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
