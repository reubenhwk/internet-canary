#!/usr/bin/env python3

from setuptools import setup
import pathlib
import sqlite3
import shutil
import yaml

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

def setup_db():

    config = yaml.load(open('/etc/internet-canary.d/internet-canary.yaml').read())

    dbpath = config['dbpath']
    path = pathlib.Path(dbpath)
    path.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(dbpath)
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS http_canary_results (
            target text not null,
            time real not null,
            result real not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS target_time ON http_canary_results (target, time);
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bandwidth_canary_results (
            time real not null,
            down_speed integer not null,
            up_speed integer not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS bandwidth_time ON bandwidth_canary_results (time);
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_canary_results (
            target text not null,
            time real not null,
            result real not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS dns_time ON dns_canary_results (time);
    ''')

    db.commit()
    shutil.chown(dbpath, 'www-data')

setup_db()
