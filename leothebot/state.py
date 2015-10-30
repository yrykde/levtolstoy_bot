#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml


class AppState(object):
    '''Singleton which stores global app state.
    '''

    config = None
    actors = None
    runtime = None

    _config_file = None

    def __init__(self):
        self.config = {}
        self.actors = {}
        self.runtime = {}

    def load_config(self, config_file=None):
        if config_file is None:
            if self._config_file is None:
                raise ValueError('Config file was not specified')
            config_file = self._config_file

        with open(config_file, 'rb') as config_f:
            config = yaml.load(config_f)
            self._config_file = config_file
        self.config.update(config)


state = AppState()
