#!/usr/bin/env python
# -*- coding: utf-8 -*-

import treq
import mock
from twisted.internet import defer
from twisted.trial import unittest

from leothebot import translate


class TranslateSmokeTest(unittest.TestCase):
    def setUp(self):
        self.translate_api = translate.TranslateAPI(token="abcdef")
        self.treq_get = translate.treq.get = \
            mock.Mock(return_value=defer.succeed(
                mock.Mock(return_value=defer.succeed('{}'))))

    @defer.inlineCallbacks
    def test_languages(self):
        yield self.translate_api.languages()

        self.assertTrue(self.treq_get.called)

    @defer.inlineCallbacks
    def test_detect(self):
        yield self.translate_api.detect(text="this is a text")

        self.assertTrue(self.treq_get.called)

    @defer.inlineCallbacks
    def test_translate(self):
        yield self.translate_api.translate(
            text="text", source="en", target="de")

        self.assertTrue(self.treq_get.called)
