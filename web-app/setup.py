#!/usr/bin/env python3

from setuptools import setup

setup(name='InternetCanaryWebApp',
    version='2.0',
    packages=['InternetCanaryWebApp'],
    include_package_data=True,
    zip_safe=False,
    data_files=[
        ('/var/www/InternetCanaryWebApp', ['InternetCanaryWebApp.wsgi']),
        ('/etc/httpd/conf.d', ['InternetCanaryWebApp.conf']),
    ]
)

