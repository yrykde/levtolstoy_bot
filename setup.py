#!/usr/bin/env python

from distutils.core import setup

install_requires = (
    'paramiko',
    'requests',
    'flask',
)

tests_require = (
    'moto',
    'pylint',
    'pep8',
)

setup(
    name="levtolstoy_bot",
    version="0.0.1",
    url='https://github.com/tonylazarew/levtolstoy_bot',
    author='Anton Lazarev',
    author_email='tony@lazarew.me',
    description=('Blah blah bot'),
    license='None',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Console',
        'Framework :: Flask',
    ],
    packages=[
        'leothebot',
        'leothebot.leo',
        'leothebot.quotes',
        'leothebot.telegram',
    ],
    scripts=['levtolstoy'],
)
