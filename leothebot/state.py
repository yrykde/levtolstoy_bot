#!/usr/bin/env python
# -*- coding: utf-8 -*-


class AppState(object):
    '''Singleton which stores global app state.
    '''

    config = {}
    actors = {}


state = AppState()
