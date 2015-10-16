#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Leo's brains, coupled to Telegram's data model
# author: tony@lazarew.me


import random

from twisted.internet import reactor, defer

from . import quotes
from state import state as singleton_state


def reactor_sleep(sleep_time):
    """Reactor based sleep()."""
    d = defer.Deferred()
    reactor.callLater(sleep_time, d.callback, None)
    return d


class Leo(object):
    def __init__(self, telegram, state=None, quotes=None):
        self.telegram = telegram

        if quotes is None:
            quotes = quotes.QuoteFetcher()
        self.quotes = quotes

        if state is None:
            state = singleton_state
        self.state = state

        self._config = self.state.config['leo_brain']

    #
    # State persistence between service restarts
    #

    def restore_state(self):
        pass

    def persist_state(self):
        pass

    #
    # Incoming triggers processing
    #

    def reaction_delay(self, payload):
        """Realistic incoming messages reaction delay.

        TODO(tony): definitely depending on which chat we got the message in
        and probably depending on who sent it.
        """
        return reactor_sleep(random.randint(2, 6))

    @defer.inlineCallbacks
    def incoming_message(self, payload):
        print("payload=%r" % payload)
        chat_id = payload['message']['chat']['id']
        reply_to_message_id = random.choice(
            (None, payload['message']['message_id']))

        quote = yield self.quotes.get_quote()

        # Simulating reaction
        yield self.reaction_delay(payload)

        yield self.send_message(
            chat_id=chat_id,
            text=quote,
            reply_to_message_id=reply_to_message_id)

        defer.returnValue(None)

    #
    # Output methods with realistic chat actions
    #

    @defer.inlineCallbacks
    def send_message(self, chat_id, text, **kw):
        # Simulate typing
        typing_delay = int(self._config['typing_speed'] * len(text))
        print('typing for %d sec' % typing_delay)

        # After a while chat action does expire. This loop makes sure
        # that it is being updated regularly.
        for i in range(0, typing_delay + 1, 3):
            yield self.telegram.send_chat_action(
                chat_id=chat_id,
                action='typing')

            iteration_time = 3 if typing_delay - i >= 3 else typing_delay - i

            yield reactor_sleep(iteration_time)

            # Simulate pauses humans do while typing (to think?)
            if random.randint(1, 10) == 1:
                yield reactor_sleep(10)

        yield self.telegram.send_message(chat_id=chat_id, text=text, **kw)
