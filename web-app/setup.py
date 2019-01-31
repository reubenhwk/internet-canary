#!/usr/bin/env python

from setuptools import setup

setup(name='HelloFlask',
    version='2.0',
    packages=['helloflask'],
    include_package_data=True,
    zip_safe=False,
    data_files=[
        ('/var/www/helloflask', ['helloflask.wsgi']),
        ('/etc/httpd/conf.d', ['helloflask.conf']),
    ]
)

