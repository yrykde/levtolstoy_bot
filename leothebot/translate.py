#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Google Translate API v2
# author: tony@lazarew.me

import treq

from twisted.internet import defer


def ensure_utf8(params):
    for k, v in params.items():
        params[k] = unicode(v).encode('utf-8')
    return params


class TranslateAPI(object):
    endpoint = "https://www.googleapis.com/language/translate/v2"

    def __init__(self, token):
        self.token = token

    @defer.inlineCallbacks
    def send(self, uri='', params=None):
        if params is None:
            params = {}

        params['key'] = self.token
        params.setdefault('prettyprint', 'false')

        url = "{0}{1}".format(self.endpoint, uri)
        response = yield treq.get(
            url=url, params=ensure_utf8(params))

        content = yield response.json()
        defer.returnValue(content)

    def languages(self):
        return self.send(uri='/languages')

    def translate(self, text, source, target):
        return self.send(params={
                'q': text,
                'source': source,
                'target': target,
            })

    def detect(self, text):
        return self.send(uri='/detect', params={'q': text})
