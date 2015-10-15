#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import levtolstoy


class WebhookCodeGeneratorTests(unittest.TestCase):
    def test_lengths(self):
        meth = levtolstoy.generate_webhook_code

        self.assertEqual(len(meth(10)), 10)
        self.assertEqual(len(meth(30)), 30)
        self.assertEqual(len(meth(100)), 100)

    def test_randomness(self):
        meth = levtolstoy.generate_webhook_code

        code1 = meth(70)
        code2 = meth(70)
        self.assertNotEqual(code1, code2)

        code1 = meth(5)
        code2 = meth(5)
        self.assertNotEqual(code1, code2)
