#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import unittest

from leothebot import state

test_config_1 = """
---
server:
    telegram_token: "x"
    host: "y"
    port: 80
    root_url: "https://localhost"
    certificate:
        |
        blabla

"""

test_config_dict_1 = {
    'server': {
        'telegram_token': 'x',
        'host': 'y',
        'port': 80,
        'root_url': 'https://localhost',
        'certificate': 'blabla\n',
    }
}

test_config_2_addition = """
updated_field: value
"""

test_config_dict_2_addition = {'updated_field': 'value'}


test_config_3 = """
---
server:
    telegram_token: "x"
    host: zzz
    port: 5505
    root_url: "https://localhost"
    certificate:
        |
        blabla

"""

test_config_dict_3 = {
    'server': {
        'telegram_token': 'x',
        'host': 'zzz',
        'port': 5505,
        'root_url': 'https://localhost',
        'certificate': 'blabla\n',
    }
}

test_config_4 = """
---
server:
    telegram_token: "x"
    certificate:
        |
        blabla

"""

test_config_dict_4 = {
    'server': {
        'telegram_token': 'x',
        'certificate': 'blabla\n',
    }
}


class AppStateSingletonTest(unittest.TestCase):
    def test_singleton(self):
        self.assertIsInstance(state.state, state.AppState)


class ConfigurationLoadTest(unittest.TestCase):
    def setUp(self):
        # Testing as a normal class, not singleton
        self.state = state.AppState()

    def test_reload_config_add_field(self):
        config_file = tempfile.NamedTemporaryFile()
        config_file.write(test_config_1)
        config_file.flush()

        self.state.load_config(config_file.name)
        self.assertDictEqual(test_config_dict_1, self.state.config)

        config_file.write(test_config_2_addition)
        config_file.flush()

        self.state.load_config()
        self.assertDictContainsSubset(
            test_config_dict_2_addition, self.state.config)

    def test_reload_config_update_field(self):
        config_file = tempfile.NamedTemporaryFile()
        config_file.write(test_config_1)
        config_file.flush()

        self.state.load_config(config_file.name)
        self.assertDictEqual(test_config_dict_1, self.state.config)

        config_file.seek(0)
        config_file.write(test_config_3)
        config_file.flush()

        self.state.load_config()
        self.assertDictEqual(test_config_dict_3, self.state.config)

    def test_reload_config_remove_field(self):
        config_file = tempfile.NamedTemporaryFile()
        config_file.write(test_config_1)
        config_file.flush()

        self.state.load_config(config_file.name)
        self.assertDictEqual(test_config_dict_1, self.state.config)

        config_file = tempfile.NamedTemporaryFile()
        config_file.write(test_config_4)
        config_file.flush()

        self.state.load_config(config_file.name)
        self.assertDictEqual(test_config_dict_4, self.state.config)
