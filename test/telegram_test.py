#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest as sync_unittest
from twisted.internet import defer
from twisted.trial import unittest as async_unittest

from leothebot import telegram


class TelegramAsyncSmokeTest(async_unittest.TestCase):
    def setUp(self):
        self.telegram_api = telegram.TelegramAPI(token="abcdef")
        self.post = telegram.treq.post = \
            mock.Mock(return_value=defer.succeed(
                mock.Mock(return_value=defer.succeed('{}'))))

    @defer.inlineCallbacks
    def test_send_message(self):
        yield self.telegram_api.send_message(chat_id='1', text='text')

        self.assertTrue(self.post.called)

    @defer.inlineCallbacks
    def test_send_chat_action(self):
        yield self.telegram_api.send_chat_action(chat_id='1', action='typing')

        self.assertTrue(self.post.called)


class TelegramSyncSmokeTest(sync_unittest.TestCase):
    def setUp(self):
        self.telegram_api = telegram.TelegramAPI(token="abcdef")

        self.response = mock.Mock()
        self.post = telegram.requests.post = \
            mock.Mock(return_value=self.response)

    def test_initialize_webhook(self):
        self.response.ok = True
        self.telegram_api.initialize_webhook(
            endpoint="http://", certificate="cert")

        self.assertTrue(self.post.called)

        self.response.ok = False
        with self.assertRaises(telegram.TelegramAPIError):
            self.telegram_api.initialize_webhook(
                endpoint="http://", certificate="cert")

    def test_disable_webhook(self):
        self.response.ok = True
        self.telegram_api.disable_webhook()

        self.assertTrue(self.post.called)

        self.response.ok = False
        with self.assertRaises(telegram.TelegramAPIError):
            self.telegram_api.disable_webhook()
