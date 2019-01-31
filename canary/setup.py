#!/usr/bin/env python

from setuptools import setup

setup(name='InternetCanary',
    version='1.0',
    packages=['InternetCanary'],
    zip_safe=False,
    data_files=[
        ('/lib/systemd/system', ['internet-canary.service']),
        ('/etc/internet-canary.d', ['internet-canary.json']),
        ('/usr/bin', ['internet-canary.py']),
    ]
)

