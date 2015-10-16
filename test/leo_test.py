#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
from twisted.internet import defer
from twisted.trial import unittest

from leothebot import leo, telegram, state, quotes

mock_payload_1 =  {
    u'message': {
        u'date': 1444986554,
        u'text': u'text',
        u'from': {
            u'first_name': u'John',
            u'last_name': u'Doe',
            u'id': 1111111
        },
        u'message_id': 179,
        u'chat': {
            u'type': u'group',
            u'id': -1111111,
            u'title': u'leo test'
        }
    },
    u'update_id': 861138601
}


def get_quote_mock():
    d = defer.Deferred()
    d.callback('quote')
    return d


class IncomingMessageSmokeTest(unittest.TestCase):
    def setUp(self):
        self.telegram_mock = mock.Mock(spec_set=telegram.TelegramAPI)
        self.state = state.AppState()
        self.state.config['leo_brain'] = {}
        self.quotes = mock.Mock(spec_set=quotes.QuoteFetcher)
        self.quotes.get_quote = get_quote_mock
        self.leo = leo.Leo(
            telegram=self.telegram_mock,
            state=self.state,
            quotes=self.quotes)

    @defer.inlineCallbacks
    def test_incoming_message(self):
        self.state.config['leo_brain']['typing_speed'] = 0.0001
        yield self.leo.incoming_message(payload=mock_payload_1)

