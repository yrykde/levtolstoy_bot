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

        self.json_mock = mock.Mock()
        response = mock.Mock()
        response.json = self.json_mock
        self.treq_get = translate.treq.get = \
            mock.Mock(return_value=defer.succeed(response))

    @defer.inlineCallbacks
    def test_languages(self):
        self.json_mock.return_value = defer.succeed(
            {'data': {'languages': [{'language': 'en'}]}})
        expected_data = {'en': None}
        result = yield self.translate_api.languages()

        self.assertTrue(self.treq_get.called)
        self.assertDictEqual(expected_data, result)

    @defer.inlineCallbacks
    def test_languages_target(self):
        self.json_mock.return_value = defer.succeed(
            {'data': {'languages': [{'name': 'english', 'language': 'en'}]}})
        expected_data = {'en': 'english'}
        result = yield self.translate_api.languages(target='en')

        self.assertTrue(self.treq_get.called)
        self.assertDictEqual(expected_data, result)

        self.assertTrue(self.treq_get.called)

    @defer.inlineCallbacks
    def test_languages_fail(self):
        self.json_mock.return_value = defer.succeed({})
        with self.assertRaises(translate.TranslateAPIError):
            yield self.translate_api.languages()

    @defer.inlineCallbacks
    def test_detect(self):
        yield self.translate_api.detect(text="this is a text")

        self.assertTrue(self.treq_get.called)

    @defer.inlineCallbacks
    def test_translate(self):
        yield self.translate_api.translate(
            text="text", source="en", target="de")

        self.assertTrue(self.treq_get.called)
