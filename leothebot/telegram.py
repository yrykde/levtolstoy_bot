#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Adhoc Telegram API
# author: tony@lazarew.me

import requests


class TelegramAPIError(Exception):
    pass


class TelegramAPI(object):
    endpoint = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token

    def send(self, command, params=None, files=None):
        url = "{0}{1}/{2}".format(
            self.endpoint,
            self.token,
            command)
        response = requests.post(url=url, data=params, files=files)

        if not response.ok:
            raise TelegramAPIError

        return response.json()

    def initialize_webhook(self, endpoint, certificate):
        self.send(
            command='setWebhook',
            params={'url': endpoint},
            files={"certificate": ('certificate', certificate)})

    def disable_webhook(self):
        self.send(
            command="setWebhook",
            params={"url": ""})

