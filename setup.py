#!/usr/bin/env python3

from setuptools import setup

setup(name='InternetCanary',
    version='3.0',
    packages=['InternetCanary'],
    zip_safe=False,
    include_package_data=True,
    data_files=[
        ('/lib/systemd/system', ['internet-canary.service']),
        ('/etc/internet-canary.d', ['internet-canary.yaml']),
        ('/usr/bin', ['internet-canary.py']),
        ('/var/www/InternetCanaryWebApp', ['InternetCanaryWebApp.wsgi']),
        ('/etc/apache2/sites-available', ['InternetCanaryWebApp.conf']),
    ]
)

