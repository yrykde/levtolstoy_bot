#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get a random smart quote from the internets
# author: tony@lazarew.me

import random
import time
import treq

from twisted.internet import reactor, defer


QUOTE_API_ENDPOINT = "http://api.forismatic.com/api/1.0/"


class QuoteFetcher(object):
    def __init__(self, lang='ru'):
        self._lang = lang

    @defer.inlineCallbacks
    def get_quote(self):
        random.seed(time.time())

        quote_params = {
            'method': 'getQuote',
            'key': '{0}'.format(random.randint(100, 999999)),
            'format': 'json',
            'lang': self._lang}

        response = yield treq.post(
            url=QUOTE_API_ENDPOINT,
            data=quote_params)

        quote = "пукнул, сорян"

        content = yield response.json()

        try:
            quote = content['quoteText']
        except KeyError:
            pass

        defer.returnValue(quote)
