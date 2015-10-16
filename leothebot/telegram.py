#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Adhoc Telegram API
# author: tony@lazarew.me

import requests
import treq

from twisted.internet import defer



class TelegramAPIError(Exception):
    pass


def ensure_utf8(params):
    for k, v in params.items():
        params[k] = unicode(v).encode('utf-8')
    return params


class TelegramAPI(object):

    _chat_actions = (
        'typing',
        'upload_photo',
        'record_video',
        'upload_video',
        'record_audio',
        'upload_audio',
        'upload_document',
        'find_location',
    )

    endpoint = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token


    #
    # Blocking code (executed before/after reactor)
    #

    def send_blocking(self, command, params=None, files=None):
        url = "{0}{1}/{2}".format(
            self.endpoint,
            self.token,
            command)
        response = requests.post(
            url=url, data=ensure_utf8(params), files=files)

        if not response.ok:
            raise TelegramAPIError

        return response.json()

    def initialize_webhook(self, endpoint, certificate):
        r = self.send_blocking(
            command='setWebhook',
            params={'url': endpoint},
            files={'certificate': ('certificate', certificate)})
        print(r)

    def disable_webhook(self):
        # This
        r = self.send_blocking(
            command="setWebhook",
            params={"url": ""})
        print(r)

    #
    # Non-blocking code
    #

    @defer.inlineCallbacks
    def send(self, command, params=None, files=None):
        url = "{0}{1}/{2}".format(
            self.endpoint,
            self.token,
            command)
        response = yield treq.post(
            url=url, data=ensure_utf8(params), files=files)

        content = yield response.json()
        defer.returnValue(content)

    def send_message(self, chat_id, text, **kw):
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        params.update(kw)

        return self.send('sendMessage', params=params)

    def send_chat_action(self, chat_id, action):
        if action not in self._chat_actions:
            return defer.fail("")

        params = {
            'chat_id': chat_id,
            'action': action,
        }

        return self.send('sendChatAction', params=params)
