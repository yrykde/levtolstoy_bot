#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Leo's brains, coupled to Telegram's data model
# author: tony@lazarew.me


import random

from twisted.internet.defer import inlineCallbacks, returnValue

from . import quotes
from state import state

class Leo(object):
    def __init__(self, telegram):
        self.telegram = telegram

        self.quotes = quotes.QuoteFetcher()

    #
    # Incoming triggers processing
    #

    @inlineCallbacks
    def incoming_message(self, payload):
        print("payload= %r" % payload)
        print(id(state))
        returnValue(None)

    #
    # State persistence between service restarts
    #

    def restore_state(self):
        pass

    def persist_state(self):
        pass
