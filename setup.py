#!/usr/bin/env python

from distutils.core import setup

install_requires = (
    'paramiko',
    'requests',
    'pyyaml',
    'klein',
    'treq',
    'twisted',
    'nltk',
)

tests_require = (
    'mock',
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
        'Framework :: Klein',
        'Framework :: Twisted',
    ],
    packages=[
        'leothebot',
    ],
    scripts=['levtolstoy'],
)
