#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get a random smart quote from the internets
# author: tony@lazarew.me

import random
import requests


QUOTE_API_ENDPOINT = "http://api.forismatic.com/api/1.0/"


class QuoteFetcher(object):
    def __init__(self, lang='ru'):
        self._lang = lang

    def get_quote(self):
        random.seed(time.time())

        quote_params = {
            'method': 'getQuote',
            'key': '{0}'.format(random.randint(100, 999999)),
            'format': 'json',
            'lang': self._lang}

        response = requests.post(
            url=QUOTE_API_ENDPOINT,
            data=quote_params)

        quote = "пукнул, сорян"

        if not response.ok:
            return quote

        try:
            quote = response.json()['quoteText']
        except KeyError:
            pass

        return quote
